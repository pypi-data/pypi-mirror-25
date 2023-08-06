#!/usr/bin/env python
'''
Inner objects to formalize kubernetes responses.
The logical structure of ockle is illustrated as:

        OCKLE           layer-0
------------------------
    APPLICATIONS        layer-1
------------------------
      INSTANCES         layer-2

Layer-2 is elementary abstractions provided by kubernetes say HDFS, ZK, Inceptor etc.
Layer-1 is an application-perspective organization of elementary abstractions to
mask dependence details of a specific applications. E.g., an application APP-HDFS in
layer-1 is mapped to HDFS + ZK in layer-2 when automatically by deducing some
underlying dependencies.

Their logical relationships are modeled by:
K8S
 |___Tenant
 |___Application (layer-1)
     |___Instance (layer-2)
         |___Services
         |___Pods
'''
import re

from . import k8s_base_config
from libappadapter.k8s.utils import amount_to_float, format_amount
from libappadapter.k8s.status import ApplicationRunningStatus, InstanceRunningStatus, PodRunningStatus, ContainerRunningStatus

__all__ = ['TenantObject', 'InstanceObject', 'ApplicationObject', 'ServiceObject',
           'PodObject', 'NodeObject', 'StatefulSetObject', 'DeploymentObject', 'EventObject']

label_control_prefix = k8s_base_config.instance_control_label_prefix
label_prefix = k8s_base_config.instance_label_prefix


class TenantObject(object):
    def __init__(self, tenant_model):
        self.tenant_name = tenant_model.metadata.name
        self.tenant_uid = tenant_model.metadata.uid
        self.tenant_creation_time = tenant_model.metadata.creation_timestamp
        self.tenant_labels = tenant_model.metadata.labels
        self.tenant_status = tenant_model.status.phase.upper()

    def to_dict(self):
        return {
            'tenant_name': self.tenant_name,
            'tenant_uuid': self.tenant_uid,
            'tenant_creation_time': self.tenant_creation_time,
            'tenant_status': self.tenant_status
        }


class ApplicationObject(object):
    def __init__(self, app_model):
        annotations = app_model.metadata.annotations if app_model.metadata else None
        if annotations is None:
            annotations = {}
        self.application_id = None
        self.application_name = annotations.get('application_name', None)
        self.application_type = annotations.get('application_type', None)
        self.cluster_id = int(annotations.get('cluster_id', '-1'))

        self.running_status = None

        self.instances = []  # a list of InstanceObjects

    def is_ready(self):
        """
        The application will be ready once all instances are running successfully.
        :return: True or False
        """
        status = [i.is_ready() for i in self.instances]
        if len(status) == 0 or False in status:
            return False
        return True

    def get_status(self):
        """
        Get application status according to status of instances
        :return: RunningStatus
        """
        status_cnt = {
            InstanceRunningStatus.DEPLOYING: 0,
            InstanceRunningStatus.PENDING: 0,
            InstanceRunningStatus.CREATING: 0,
            InstanceRunningStatus.TERMINATING: 0,
            InstanceRunningStatus.WAITING: 0,
            InstanceRunningStatus.UNREADY: 0,
            InstanceRunningStatus.RUNNINGERROR: 0,
            InstanceRunningStatus.RUNNING: 0,
            InstanceRunningStatus.TERMINATED: 0
        }

        if len(self.instances) == 0:
            self.running_status = ApplicationRunningStatus.TERMINATED
            return self.running_status

        for instance in self.instances:
            instance_status = instance.running_status if instance.running_status else instance.get_status()
            if instance_status in status_cnt:
                status_cnt[instance_status] += 1

        if status_cnt.get(InstanceRunningStatus.DEPLOYING) > 0:
            self.running_status = ApplicationRunningStatus.DEPLOYING

        elif status_cnt[InstanceRunningStatus.PENDING] > 0:
            self.running_status = ApplicationRunningStatus.PENDING

        elif status_cnt[InstanceRunningStatus.CREATING] > 0:
            self.running_status = ApplicationRunningStatus.CREATING

        elif status_cnt.get(InstanceRunningStatus.TERMINATING) > 0:
            self.running_status = ApplicationRunningStatus.TERMINATING

        elif status_cnt.get(InstanceRunningStatus.WAITING) > 0:
            self.running_status = ApplicationRunningStatus.WAITING

        elif status_cnt.get(InstanceRunningStatus.UNREADY) > 0:
            self.running_status = ApplicationRunningStatus.UNREADY

        elif status_cnt.get(InstanceRunningStatus.RUNNINGERROR) > 0 or \
                (status_cnt.get(InstanceRunningStatus.TERMINATED) > 0 and status_cnt.get(InstanceRunningStatus.RUNNING) > 0):
            self.running_status = ApplicationRunningStatus.RUNNINGERROR

        elif status_cnt.get(InstanceRunningStatus.RUNNING) > 0:
            self.running_status = ApplicationRunningStatus.RUNNING

        else:
            self.running_status = ApplicationRunningStatus.TERMINATED

        return self.running_status

    def to_dict(self):
        return {
            'application_id': self.application_id,
            'application_name': self.application_name,
            'application_type': self.application_type,
            'application_status': "Ready" if self.is_ready() else "Not Ready",
            'instances': [i.to_dict() for i in self.instances],
        }


class InstanceObject(object):
    def __init__(self, instance_model):
        metadata = instance_model.metadata
        status = instance_model.status
        spec = instance_model.spec

        if metadata:
            self.instance_name = metadata.name if metadata.name else ''
            self.instance_type = metadata.labels.get(label_prefix, '') if metadata.labels else ''
            self.cluster_id = int(metadata.annotations.get('cluster_id', '-1')) if metadata.annotations else -1
            self.system_context_instance_id = \
                int(metadata.annotations.get('system_context_instance_id', '-1')) if metadata.annotations else -1
        else:
            self.instance_name = ''
            self.instance_type = ''
            self.cluster_id = -1
            self.system_context_instance_id = -1
        if status:
            self.instance_status = status.phase.upper() if status.phase else ''
            self.instance_is_ready = status.ready if status.ready else False
            self.modules = status.modules if status.modules else []
        else:
            self.instance_status = ''
            self.instance_is_ready = False
            self.modules = []
        if spec:
            self.instance_id = spec.instance_id
            self.configs = spec.configs
            self.version = spec.application_ref.version
        else:
            self.instance_id = None
            self.configs = None
            self.version = None

        self.running_status = None
        self.pods = []
        self.services = []
        self.stateful_sets = []
        self.deployments = []

    def is_ready(self):
        status = [p.is_ready for p in self.pods]
        if len(status) == 0 or False in status:
            return False
        return True

    def get_status(self):
        """
        Get instance status according to status of pods. stateful sets, and deployments
        :return: RunningStatus
        """
        # status of instance
        if self.instance_status != InstanceRunningStatus.RUNNING:
            self.running_status = self.instance_status
            return self.instance_status

        # status of existing pods
        status_cnt = {
            PodRunningStatus.PENDING: 0,
            PodRunningStatus.CREATING: 0,
            PodRunningStatus.TERMINATING: 0,
            PodRunningStatus.WAITING: 0,
            PodRunningStatus.UNREADY: 0,
            PodRunningStatus.RUNNINGERROR: 0,
            PodRunningStatus.RUNNING: 0,
            PodRunningStatus.TERMINATED: 0
        }

        if len(self.pods) == 0:
            self.running_status = InstanceRunningStatus.TERMINATED
            return self.running_status

        for pod in self.pods:
            status = pod.running_status if pod.running_status else pod.get_status()
            if status in status_cnt:
                status_cnt[status] += 1

        if status_cnt.get(PodRunningStatus.PENDING) > 0:
            self.running_status = InstanceRunningStatus.PENDING

        elif status_cnt.get(PodRunningStatus.CREATING) > 0:
            self.running_status = InstanceRunningStatus.CREATING

        elif status_cnt.get(PodRunningStatus.TERMINATING) > 0:
            self.running_status = InstanceRunningStatus.TERMINATING

        elif status_cnt.get(PodRunningStatus.WAITING) > 0:
            self.running_status = InstanceRunningStatus.WAITING

        elif status_cnt.get(PodRunningStatus.UNREADY) > 0:
            self.running_status = InstanceRunningStatus.UNREADY

        elif status_cnt.get(PodRunningStatus.TERMINATED) > 0:
            self.running_status = InstanceRunningStatus.TERMINATED

        if self.running_status:
            return self.running_status

        status_cnt[PodRunningStatus.RUNNING] = 0
        # status of stateful_sets
        for stateful_set in self.stateful_sets:
            stateful_set_status = stateful_set.get_status()
            if stateful_set_status in status_cnt:
                status_cnt[stateful_set_status] += 1

        # status of deployments
        for deployment in self.deployments:
            deployment_status = deployment.get_status()
            if deployment_status in status_cnt:
                status_cnt[deployment_status] += 1

        if status_cnt.get(PodRunningStatus.UNREADY) > 0:
            self.running_status = InstanceRunningStatus.UNREADY

        elif status_cnt.get(PodRunningStatus.TERMINATING) > 0:
            self.running_status = InstanceRunningStatus.TERMINATING

        elif status_cnt.get(PodRunningStatus.RUNNINGERROR) > 0 or \
                (status_cnt.get(PodRunningStatus.TERMINATED) > 0 and status_cnt.get(PodRunningStatus.RUNNING) > 0):
            self.running_status = InstanceRunningStatus.RUNNINGERROR

        elif status_cnt.get(PodRunningStatus.RUNNING) > 0:
            self.running_status = InstanceRunningStatus.RUNNING

        else:
            self.running_status = InstanceRunningStatus.TERMINATED

        return self.running_status

    def to_dict(self):
        return {
            'instance_name': self.instance_name,
            'instance_type': self.instance_type,
            'instance_status': self.instance_status,
            'pods': [p.to_dict() for p in self.pods],
            'services': [s.to_dict() for s in self.services],
            'stateful_sets': [ss.to_dict() for ss in self.stateful_sets],
            'deployments': [d.to_dict() for d in self.deployments]
        }


class ServiceObject(object):
    service_host_name_suffix = '.svc.transwarp.local'
    service_type_nodeport = 'NodePort'
    service_type_clusterip = 'ClusterIP'

    def __init__(self, service_model):
        metadata = service_model.metadata
        spec = service_model.spec

        if metadata:
            self.service_name = metadata.name if metadata.name else ''
            self.service_namespace = metadata.namespace if metadata.namespace else ''
            self.install_instance = metadata.labels.get(label_control_prefix, '') if metadata.labels else ''
            self.service_source = metadata.labels.get(label_prefix, '') if metadata.labels else ''
        else:
            self.service_name = ''
            self.service_namespace = ''
            self.install_instance = ''
            self.service_source = ''

        self.host_name = self.service_name + '.' + self.service_namespace + ServiceObject.service_host_name_suffix
        self.ports = []
        self.service_type = spec.type if spec and spec.type else ''
        ports = spec.ports if spec else None
        if ports is not None:
            for port in ports:
                self.ports.append({
                    'name': port.name if port.name else '',
                    'port': port.port if port.port else -1,
                    'node_port': port.node_port if port.node_port else -1,
                    'protocol': port.protocol if port.protocol else ''
                })

    def to_dict(self):
        return {
            'service_name': self.service_name,
            'service_type': self.service_type,
            'service_hostname': self.host_name,
            'service_source': self.service_source,
            'ports': self.ports
        }


class StatefulSetObject(object):
    def __init__(self, deployment_model):
        metadata = deployment_model.metadata
        spec = deployment_model.spec
        status = deployment_model.status

        self.replicas = spec.replicas if spec and spec.replicas else 0
        self.available_replicas = status.available_replicas if status and status.available_replicas else 0
        if metadata:
            self.stateful_set_name = metadata.name if metadata.name else ''
            self.install_instance = metadata.labels.get(label_control_prefix, '') if metadata.labels else ''
        else:
            self.stateful_set_name = ''
            self.install_instance = ''

    def get_status(self):
        if self.replicas == 0 and self.available_replicas > 0:
            return PodRunningStatus.TERMINATING
        if self.replicas == 0:
            return PodRunningStatus.TERMINATED
        if self.replicas > self.available_replicas:
            return PodRunningStatus.UNREADY
        if self.replicas == self.available_replicas:
            return PodRunningStatus.RUNNING
        return PodRunningStatus.RUNNINGERROR

    def to_dict(self):
        return {
            'stateful_set_name': self.stateful_set_name,
            'install_instance_id': self.install_instance,
            'replicas': self.replicas,
            'available_replicas': self.available_replicas
        }


class DeploymentObject(object):
    def __init__(self, deployment_model):
        metadata = deployment_model.metadata
        spec = deployment_model.spec
        status = deployment_model.status

        self.replicas = spec.replicas if spec and spec.replicas else 0
        self.available_replicas = status.available_replicas if status and status.available_replicas else 0

        if metadata:
            self.deployment_name = metadata.name if metadata.name else ''
            self.install_instance = metadata.labels.get(label_control_prefix, '') if metadata.labels else ''
        else:
            self.deployment_name = ''
            self.install_instance = ''

    def get_status(self):
        if self.replicas == 0 and self.available_replicas > 0:
            return PodRunningStatus.TERMINATING
        if self.replicas == 0:
            return PodRunningStatus.TERMINATED
        if self.replicas > self.available_replicas:
            return PodRunningStatus.UNREADY
        if self.replicas == self.available_replicas:
            return PodRunningStatus.RUNNING
        return PodRunningStatus.RUNNINGERROR

    def to_dict(self):
        return {
            'deployment_name': self.deployment_name,
            'install_instance_id': self.install_instance,
            'replicas': self.replicas,
            'available_replicas': self.available_replicas
        }


class PodObject(object):
    container_id_length = 12
    container_id_pattern = r'docker://(.+)'

    def __init__(self, pod_model):
        metadata = pod_model.metadata
        spec = pod_model.spec
        status = pod_model.status

        if metadata:
            self.pod_name = metadata.name if metadata.name else ''
            self.install_instance = metadata.labels.get(label_control_prefix, '') if metadata.labels else ''
            self.pod_type = metadata.labels.get(label_prefix, '') if metadata.labels else ''
        else:
            self.pod_name = ''
            self.install_instance = ''
            self.pod_type = ''
        if status:
            self.host_ip = status.host_ip if status.host_ip else ''
            self.pod_status = status.phase.upper() if status.phase else ''
            self.reason = status.reason if status.reason else ''
        else:
            self.host_ip = ''
            self.pod_status = ''
            self.reason = ''

        self.node_name = spec.node_name if spec and spec.node_name else ''
        self.instance_name = ''
        self.cpu_limit = amount_to_float(0)
        self.cpu_request = amount_to_float(0)
        self.mem_limit = amount_to_float(0)
        self.mem_request = amount_to_float(0)
        self.running_status = None
        self.is_ready = True

        self.image = None
        self.events = []

        # manipulate containers
        self.containers_status = {}

        containers = spec.containers if spec else []

        for container in containers:
            if container.image is not None:
                self.image = container.image
                break

        for container in containers:
            resources = container.resources
            if resources and resources.limits:
                self.cpu_limit = amount_to_float(resources.limits.get('cpu', 0))
                self.mem_limit = amount_to_float(resources.limits.get('memory', 0))
            if resources and resources.requests:
                self.cpu_request = amount_to_float(resources.requests.get('cpu', 0))
                self.mem_request = amount_to_float(resources.requests.get('memory', 0))

            container_id = ''
            container_status_val = ContainerRunningStatus.PENDING
            container_status_reason = ''
            container_is_ready = False
            if status and status.container_statuses:
                for container_status in status.container_statuses:
                    if container_status.name == container.name:
                        container_id = container_status.container_id if container_status.container_id else ''
                        container_is_ready = container_status.ready
                        # Set container status
                        if container_status.state:
                            if container_status.state.running:
                                container_status_val = ContainerRunningStatus.RUNNING if container_is_ready else ContainerRunningStatus.UNREADY
                            elif container_status.state.waiting:
                                waiting_reason = container_status.state.waiting.reason
                                container_status_reason = waiting_reason.upper() if waiting_reason is not None else ''
                                if container_status_reason == 'CONTAINERTERMINATING':
                                    container_status_val = ContainerRunningStatus.TERMINATING
                                elif container_status_reason == 'CONTAINERCREATING':
                                    container_status_val = ContainerRunningStatus.CREATING
                                else:
                                    container_status_val = ContainerRunningStatus.WAITING
                            elif container_status.state.terminated:
                                terminated_reason = container_status.state.terminated.reason
                                container_status_reason = terminated_reason.upper() if terminated_reason is not None else ''
                                container_status_val = ContainerRunningStatus.TERMINATED

                        break

            if not container_is_ready:
                self.is_ready = False

            self.containers_status[container.name] = {
                'container_name': container.name,
                'container_id': self.format_container_id(container_id),
                'container_status': container_status_val,
                'container_status_reason': container_status_reason,
            }

    def get_status(self):
        """
        Get pod status according to the containers' status
        :return: RunningStatus
        """
        status_cnt = {
            ContainerRunningStatus.PENDING: 0,
            ContainerRunningStatus.CREATING: 0,
            ContainerRunningStatus.TERMINATING: 0,
            ContainerRunningStatus.WAITING: 0,
            ContainerRunningStatus.TERMINATED: 0,
            ContainerRunningStatus.UNREADY: 0,
            ContainerRunningStatus.RUNNING: 0
        }
        for container_name in self.containers_status:
            container_status = self.containers_status[container_name].get('container_status', ContainerRunningStatus.PENDING)
            if container_status in status_cnt:
                status_cnt[container_status] += 1

        if status_cnt.get(ContainerRunningStatus.PENDING) > 0:
            self.running_status = PodRunningStatus.PENDING

        elif status_cnt.get(ContainerRunningStatus.CREATING) > 0:
            self.running_status = PodRunningStatus.CREATING

        elif status_cnt.get(ContainerRunningStatus.TERMINATING) > 0:
            self.running_status = PodRunningStatus.TERMINATING

        elif status_cnt.get(ContainerRunningStatus.WAITING) > 0:
            self.running_status = PodRunningStatus.WAITING

        elif status_cnt.get(ContainerRunningStatus.TERMINATED) > 0:
            self.running_status = PodRunningStatus.TERMINATED

        elif status_cnt.get(ContainerRunningStatus.UNREADY) > 0:
            self.running_status = PodRunningStatus.UNREADY

        else:
            self.running_status = PodRunningStatus.RUNNING

        return self.running_status

    @classmethod
    def format_container_id(cls, container_id):
        container_ids = re.findall(cls.container_id_pattern, container_id)
        container_id = container_ids[0] if len(container_ids) > 0 else container_id
        return container_id[0:cls.container_id_length-1] if len(container_id) >= cls.container_id_length else container_id

    def to_dict(self):
        return {
            'pod_name': self.pod_name,
            'node_name': self.node_name,
            'host_ip': self.host_ip,
            'install_instance': self.install_instance,
            'instance_name': self.instance_name,
            'cpu_limit': self.cpu_limit,
            'cpu_request': self.cpu_request,
            'mem_limit': self.mem_limit,
            'mem_request': self.mem_request,
            'pod_status': self.pod_status,
            'reason': self.reason,
            'is_ready': self.is_ready,
            'containers_status': self.containers_status,
            'events': self.events
        }


class EventObject(object):
    def __init__(self, event_model):
        self.first_timestamp = event_model.first_timestamp
        self.last_timestamp = event_model.last_timestamp
        self.count = event_model.count
        self.type = event_model.type
        self.reason = event_model.reason
        self.message = event_model.message

        involved_object = event_model.involved_object
        self.ref_kind = involved_object.kind
        self.ref_name = involved_object.name

    def to_dict(self):
        return {
            'first_timestamp': str(self.first_timestamp),
            'last_timestamp': str(self.last_timestamp),
            'count': self.count,
            'type': self.type,
            'reason': self.reason,
            'message': self.message
        }


class NodeObject(object):
    def __init__(self, node_model):
        self.node_name = node_model.metadata.name if node_model.metadata and node_model.metadata.name else ''
        allocatable = node_model.status.allocatable if node_model.status else None
        if allocatable:
            self.cpu_cores = format_amount(allocatable.get('cpu', ''))
            self.memory = format_amount(allocatable.get('memory', ''))
            self.storage = format_amount(allocatable.get('storage', ''))
        else:
            self.cpu_cores = ''
            self.memory = ''
            self.storage = ''

        self.pods = []

    def to_dict(self):
        return {
            'node_name': self.node_name,
            'cpu_cores': self.cpu_cores,
            'memory': self.memory,
            'storage': self.storage,
            'pods': [p.to_dict() for p in self.pods]
        }
