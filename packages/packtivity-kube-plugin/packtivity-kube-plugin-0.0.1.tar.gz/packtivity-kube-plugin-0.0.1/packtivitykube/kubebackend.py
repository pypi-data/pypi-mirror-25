from kubernetes import client,config
from packtivity.asyncbackends import PacktivityProxyBase
from packtivity.syncbackends import packconfig, build_job
from packtivity.statecontexts import load_state
from packtivity import prepublish_default
from yadage.utils import WithJsonRefEncoder
import logging
import uuid
import os
import jq


log = logging.getLogger(__name__)

class KubeProxy(PacktivityProxyBase):
    def __init__(self, job_id, spec, pars, state, result = None):
        self.job_id = job_id
        self.spec = spec
        self.pars = pars
        self.state = state
        self.result = result

    def proxyname(self):
        return 'KubeProxy'

    def details(self):
        return {
            'job_id': self.job_id,
            'spec': self.spec,
            'pars':self.pars,
            'state':self.state.json(),
            'result': None
        }

    @classmethod
    def fromJSON(cls,data):
        return cls(
            data['proxydetails']['job_id'],
            data['proxydetails']['spec'],
            data['proxydetails']['pars'],
            load_state(data['proxydetails']['state']),
            data['proxydetails']['result']
        )

class KubeBackend(object):
    def __init__(self,kubeconfigloc = None):
        config.load_kube_config(kubeconfigloc or os.path.join(os.environ['HOME'],'.kube/config'))
        self.config = packconfig()

    def prepublish(self, spec, parameters, state):
        return None

    def submit(self, spec, parameters, state, metadata = None):
        job = build_job(spec['process'], parameters, state, self.config)

        image   = spec['environment']['image']
        tag     = spec['environment']['imagetag']

        interpreter = 'sh' if 'command' in job else job['interpreter']
        script = job['command'] if 'command' in job else job['script']
        jobspecs = job_specs(interpreter, script, parameters, image, tag, state,
                             cvmfs = 'CVMFS' in spec['environment']['resources'],
                             parmounts = spec['environment']['par_mounts'],
                             auth = False)

        mainjobspec = jobspecs[0]
        jobid = mainjobspec['metadata']['name']
        
        thejob = client.V1Job(
            api_version = mainjobspec['apiVersion'],
            kind = mainjobspec['kind'],
            metadata = mainjobspec['metadata'],
            spec = mainjobspec['spec']
        )


        if spec['environment']['par_mounts']:
            cm_spec = jobspecs[1]
            cm = client.V1ConfigMap(api_version = 'v1', kind = 'ConfigMap', metadata = {'name': cm_spec['name']}, data = cm_spec['data'])
            client.CoreV1Api().create_namespaced_config_map('default',cm)
            log.info(cm)
            log.info('created configmap for parmounts')


        log.info(thejob)
        client.BatchV1Api().create_namespaced_job('default',thejob)                                                               

        log.info('submitted job: %s', jobid)
        return KubeProxy(
            job_id = jobid,
            spec = spec,
            pars = parameters,
            state = state
        )

    def result(self, resultproxy):
        prepub = prepublish_default(
            resultproxy.spec,resultproxy.pars, resultproxy.state
        )
        if resultproxy.result:
            log.info('found cached result %s', resultproxy.result)
            return resultproxy.result
        if prepub:
            return prepub
        log.info('cannot prepublish for job id {}.. submitting publisher pod'.format(resultproxy.job_id))
        pubdata =  publish(resultproxy.job_id,resultproxy.spec['publisher'],resultproxy.pars,resultproxy.state)
        log.info('caching result in proxy')
        resultproxy.result = pubdata
        return resultproxy.result
        


    def ready(self, resultproxy):
        jobstatus = client.BatchV1Api().read_namespaced_job(resultproxy.job_id,'default').status
        return jobstatus.failed or jobstatus.succeeded

    def successful(self, resultproxy):
        jobstatus = client.BatchV1Api().read_namespaced_job(resultproxy.job_id,'default').status
        return jobstatus.succeeded

    def fail_info(self, resultproxy):
        pass


def state_binds(state):
    container_mounts = []
    volumes = []

    log.info('mountspec: %s', state.mountspec)

    for i,path in enumerate(state.readwrite + state.readonly):
        container_mounts.append({
            "name": "packtivitystate",
            "mountPath": path,
            "subPath": path.lstrip('/')
        })

    volumes.append({
        "name": "packtivitystate",
    })
    volumes[0].update(state.mountspec)
    return container_mounts, volumes    

def cvmfs_binds():
    container_mounts = []
    volumes = []
    
    log.info('binding CVMFS')
    for repo in ['atlas.cern.ch','sft.cern.ch','atlas-condb.cern.ch']:
        reponame = repo.replace('.','').replace('-','')
        volumes.append({
            'name': reponame,
            'flexVolume': {
                'driver': "cern/cvmfs",
                'options': {
                    'repository': repo
                }
            }
        })
        container_mounts.append({
            "name": reponame,
            "mountPath": '/cvmfs/'+repo
        })
    return container_mounts, volumes

def job_specs(interpreter,script, parameters, image,imagetag,state, cvmfs, parmounts, auth):
    wrapped_script = '''cat << 'EOF' | {interpreter}\n{script}\nEOF'''.format(
        interpreter = interpreter,
        script = script)

    job_uuid = str(uuid.uuid4())

    container_mounts_state, volumes_state = state_binds(state)
    
    container_mounts = container_mounts_state
    volumes = volumes_state

    if cvmfs:
        container_mounts_cvmfs, volumes_cvmfs = cvmfs_binds()
        container_mounts += container_mounts_cvmfs
        volumes          += volumes_cvmfs

    if parmounts:
        container_mounts_pm, volumes_pm, pm_cm_spec = make_par_mount(job_uuid, parameters, parmounts)
        container_mounts += container_mounts_pm
        volumes += volumes_pm

    specs = []
    specs.append({
      "apiVersion": "batch/v1",
      "kind": "Job",
      "spec": {
        "template": {
          "spec": {
            "securityContext" : {
                "runAsUser": 0
            },
            "restartPolicy": "Never",
            "containers": [
              {
                "image": ':'.join([image,imagetag]),
                "command": [
                  "sh",
                  "-c",
                  wrapped_script
                ],
                "volumeMounts": container_mounts,
                "name": job_uuid
              }
            ],
            "volumes": volumes
          },
          "metadata": {
            "name": job_uuid
          }
        }
      },
      "metadata": {
        "name": job_uuid
      }
    })
    if parmounts:
        specs.append(pm_cm_spec)
    return specs


def make_par_mount(job_uuid, parameters, parmounts):
    parmount_configmap_contmount = []
    configmapspec = {
        'name': 'parmount-{}'.format(job_uuid),
        'data': {}
    }


    vols_by_dir_name = {}

    for i,x in enumerate(parmounts):
        configkey = 'parmount_{}'.format(i)
        configmapspec['data'][configkey] = jq.jq(x['jqscript']).transform(parameters, text_output = True)
        

        dirname = os.path.dirname(x['mountpath'])
        basename = os.path.basename(x['mountpath'])

        vols_by_dir_name.setdefault(dirname,{
            'name': 'vol-{}'.format(dirname.replace('/','-')),
            'configMap': {
                'name': configmapspec['name'],
                'items': []
            }
        })['configMap']['items'].append({
            'key': configkey, 'path': basename
        })

    log.info(vols_by_dir_name)


    for dirname,volspec in vols_by_dir_name.items():
        parmount_configmap_contmount.append({
            'name': volspec['name'],
            'mountPath':  dirname
        })
        
    return parmount_configmap_contmount, vols_by_dir_name.values(), configmapspec

import base64
import json
def publish_job(job_uuid,pubspec,parameters,state):
    pubinput = {
        'parameters': parameters,
        'state': state.json(),
        'pubspec': pubspec
    }

    wrapped_script = '''cat << 'EOF' | python /code/publish.py \n{b64data}\nEOF'''.format(
        b64data = base64.b64encode(json.dumps(pubinput, cls = WithJsonRefEncoder).encode('utf-8')).decode('utf-8')
    )

    container_mounts_state, volumes_state = state_binds(state)
    container_mounts = container_mounts_state
    volumes = volumes_state

    pubjobname = 'publish-{}'.format(job_uuid)
    spec = {
      "apiVersion": "batch/v1",
      "kind": "Job",
      "spec": {
        "template": {
          "spec": {
            "securityContext" : {
                "runAsUser": 0
            },
            "restartPolicy": "Never",
            "containers": [
              {
                "image": 'lukasheinrich/pack-kube-stateserver:latest',
                "command": [
                  "sh",
                  "-c",
                  wrapped_script
                ],
                "volumeMounts": container_mounts,
                "name": pubjobname
              }
            ],
            "volumes": volumes
          },
          "metadata": {
            "name": pubjobname
          }
        }
      },
      "metadata": {
        "name": pubjobname
      }
    }
    return spec

import time
def publish(job_uuid,pubspec,parameters,state):

    pubjobspec = publish_job(job_uuid,pubspec,parameters,state)

    thejob = client.V1Job(
        api_version = pubjobspec['apiVersion'],
        kind = pubjobspec['kind'],
        metadata = pubjobspec['metadata'],
        spec = pubjobspec['spec']
    )


    client.BatchV1Api().create_namespaced_job('default',thejob)

    log.info('submitted publishing job for %s', job_uuid)
    while True:
        log.info('checking publishing job for %s', job_uuid)
        jobstatus = client.BatchV1Api().read_namespaced_job(thejob.metadata['name'],'default').status
        if jobstatus.succeeded:
            log.info('publishing job for %s succeeded', job_uuid)
            break
        if jobstatus.failed:
            raise RuntimeError('simple publish pod failed?')
        time.sleep(0.5) 


    p = client.CoreV1Api().list_namespaced_pod('default',label_selector = 'job-name={}'.format(thejob.metadata['name'])).items[0]
    pubdata =  json.loads(base64.b64decode(client.CoreV1Api().read_namespaced_pod_log(p.metadata.name,'default')).decode('utf-8'))

    log.info('publishing job for %s published data %s', job_uuid, pubdata)
    return pubdata
