#!/usr/env/bin python
import functools
import json
import logging
import re

import tos_client
from tos_client.api_client import ApiException
from urllib3.exceptions import MaxRetryError

from libappadapter import get_kube_namespace_config
from libappadapter.exceptions import KubeException, ObjectDoesNotExist
from libappadapter.k8s.model import *
from . import k8s_base_config


logger = logging.getLogger(__name__)

__all__ = ['KubeTenantOp', 'KubeInstanceOp', 'KubeApplicationOp', 'KubeNodeOp']


def handle_tos_errors(func):
    """Decorator to process TOS exceptions"""

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except MaxRetryError, e:
            tos_server = '%s:%s' % (e.pool.host, e.pool.port)
            raise KubeException("TOS server error: failed to establish a new connection to {}".format(tos_server), 503)
        except ApiException, e:
            body = json.loads(e.body)
            message = body.get("message", "")
            raise KubeException(message, e.status)
        except KubeException, e:
            raise e
        except Exception, e:
            raise KubeException("TOS operation error: {}".format(str(e)), 500)

    return decorator


class KubeOp(object):
    """
    Base class for Kubernates operator
    """

    def __init__(self):
        tos_client.configuration.host = k8s_base_config.kubernetes_host
        tos_client.configuration.cert_file = k8s_base_config.kubernetes_client_cert
        tos_client.configuration.key_file = k8s_base_config.kubernetes_client_key
        tos_client.configuration.ssl_ca_cert = k8s_base_config.kubernetes_ca
        tos_client.configuration.verify_ssl = False


class KubeTenantOp(KubeOp):
    """
    Create and modify tenant namespace
    """

    TENANT_NAME_MAX_LENGTH = 20
    TENANT_NAME_REGEX = r'[a-z0-9]([-a-z0-9]*[a-z0-9])?'

    def __init__(self):
        super(KubeTenantOp, self).__init__()
        self.ignore_ns = ['default', 'kube-system']

    @handle_tos_errors
    def _create_namespace(self, k8s_objs):
        api_instance = tos_client.Apiv1Api()
        namespaces = []
        for (name, k8s_obj) in k8s_objs.items():
            api_response = api_instance.create_namespace(k8s_obj)
            logger.debug("Creating namespace: {}".format(str(api_response)))
            namespaces.append(TenantObject(api_response))

        return namespaces

    @handle_tos_errors
    def create_tenant(self, tenant_name, params=None):
        """
        Create a specific namespace
        :param tenant_name: the tenant to create
        :param params: a dict object with required k-v of 'tenant_name'
        :return: True or False
        """

        if not tenant_name or tenant_name in self.ignore_ns:
            raise ObjectDoesNotExist("empty tenant_name or reserved tenant name {}".format(tenant_name), 411)

        if len(tenant_name) > self.TENANT_NAME_MAX_LENGTH:
            raise KubeException('Tenant name should not be longer than {}'.format(self.TENANT_NAME_MAX_LENGTH), 411)

        if not re.match(self.TENANT_NAME_REGEX, tenant_name):
            raise KubeException('Invalid tenant name which should match "{}"'.format(self.TENANT_NAME_REGEX), 411)

        if params is None:
            params = dict()

        k8s_objs = get_kube_namespace_config(tenant_name, **params)
        logger.debug(k8s_objs.keys())

        return self._create_namespace(k8s_objs)

    @handle_tos_errors
    def update_tenant(self, tenant_name, params=None):
        """
         Update a specific namespace
         :param tenant_name: the tenant to update
         :param params: a dict object with required k-v of 'tenant_name'
         :return: True or False
         """
        # TODO: implement get_tenant according to actual demand
        pass

    @handle_tos_errors
    def get_tenant(self, tenant_name, opts=None):
        """
        Get profile of specific tenant
        :param tenant_name: a string of tenant name
        :param opts: a dict object of argument options
        :return: TenantObject or None
        """
        if tenant_name is None:
            return None

        api_instance = tos_client.Apiv1Api()
        try:
            api_response = api_instance.read_namespace(tenant_name)
        except ApiException, e:
            return None

        tenant = TenantObject(api_response)
        return tenant

    @handle_tos_errors
    def delete_tenant(self, tenant_name):
        """
        Remove specific tenant
        :param tenant_name: a string of tenant name
        :return: None
        """
        api_instance = tos_client.Apiv1Api()
        api_response = api_instance.delete_namespace('', tenant_name)
        logger.debug("Deleting namespace: {}".format(api_response))


class KubeApplicationOp(KubeOp):
    """
    Operator to manipulate kubernetes applications formation.
    The base stone is LibAppAdapter
    """

    def __init__(self):
        super(KubeApplicationOp, self).__init__()

    @handle_tos_errors
    def get_applications(self, tenant_name, application_name=None):
        """
        Get a list of application with instances.

        :param tenant_name: the tenant who operates applications
        :param application_name: a specific application name
        :return: a list of ApplicationObject
        """
        api_instance = tos_client.Apisappsv1beta1Api()
        instances_response = api_instance.list_namespaced_application_instance(tenant_name)

        applications = {}

        for item in instances_response.items:
            app = ApplicationObject(item)
            instance = InstanceObject(item)
            app_name = app.application_name

            # Filter applications by specific name
            if application_name and app.application_name != application_name:
                continue

            if app_name not in applications:
                applications[app_name] = app

            applications[app_name].instances.append(instance)

        return applications.values()


class KubeInstanceOp(KubeOp):
    """
    Operator to manipulate kubernetes instances
    """

    def __init__(self):
        super(KubeInstanceOp, self).__init__()
        self.label_control_prefix = k8s_base_config.instance_control_label_prefix

    @classmethod
    def _pprint_instance_creation_rsp(cls, instance_response):
        assert instance_response.kind == 'ApplicationInstance'
        metadata = instance_response.metadata
        spec = instance_response.spec
        status = instance_response.status

        app_name = metadata.annotations.get('application_name', '')
        app_type = metadata.annotations.get('application_type', '')
        instance_id = spec.instance_id
        phase = status.phase
        return 'instance: {0} [{1}] of application: {2} [{3}]' \
            .format(instance_id, phase, app_name, app_type)

    @classmethod
    def _pprint_instance_removal_rsp(cls, instance_response):
        status = instance_response.status
        message = instance_response.message
        return 'removal status: {}, message {}'.format(status, message)

    @classmethod
    def _pprint_instance_patch_rsp(cls, instance_response):
        spec = instance_response.spec
        instance_configs = spec.configs if spec and spec.configs else ''
        return 'instance configs: {}'.format(instance_configs)

    @handle_tos_errors
    def create_instances(self, tenant_name, k8s_instance_list):
        """
        Create application instances
        :param tenant_name: the tenant name
        :param k8s_instance_list: a list of configured instances
        :return: None
        """
        api_instance = tos_client.Apisappsv1beta1Api()
        for (key, k8s_obj) in k8s_instance_list.items():
            for i, item in enumerate(k8s_obj.get("items")):
                api_response = api_instance.create_namespaced_application_instance(item, tenant_name)
                logger.info("Creating instances: {}".format(self._pprint_instance_creation_rsp(api_response)))

    @handle_tos_errors
    def update_instances(self, tenant_name, k8s_instance_list):
        """
        Update application instances
        :param tenant_name: the tenant name
        :param k8s_instance_list: a list of configured instances
        :return: None
        """
        api_instance = tos_client.Apisappsv1beta1Api()
        for (key, k8s_obj) in k8s_instance_list.items():
            for i, item in enumerate(k8s_obj.get("items")):
                name = item.get('metadata').get('name')
                api_response = api_instance.replace_namespaced_application_instance(item, tenant_name, name)
                logger.info("Updating instances: {}".format(self._pprint_instance_creation_rsp(api_response)))

    @handle_tos_errors
    def update_or_create_instances(self, tenant_name, k8s_instance_list):
        """
        Update applications or create them if there are no existing instances
        :param tenant_name: the tenant name
        :param k8s_instance_list: a list of configured instances
        :return: None
        """
        logging.debug('TOS client:' + str(tos_client.configuration.host))
        api_instance = tos_client.Apisappsv1beta1Api()
        for (key, k8s_obj) in k8s_instance_list.items():
            for i, item in enumerate(k8s_obj.get("items")):
                try:
                    name = item.get('metadata', {}).get('name', '')
                    api_instance.read_namespaced_application_instance(tenant_name, name)
                except ApiException, e:
                    if e.status != 404:
                        raise KubeException(e.body, e.status)

                    api_response = api_instance.create_namespaced_application_instance(item, tenant_name)
                    logger.info("Creating instances: {}".format(self._pprint_instance_creation_rsp(api_response)))
                else:
                    api_response = api_instance.replace_namespaced_application_instance(item, tenant_name, name)
                    logger.info("Updating instances: {}".format(self._pprint_instance_creation_rsp(api_response)))

    @handle_tos_errors
    def delete_instances(self, tenant_name, instance_name=None):
        """Remove specific or all instances of a tenant.
        :param tenant_name: the tenant name
        :param instance_name: the instance to be removed.
            All instances will be removed if it is None.
        :return: None
        """
        api_instance = tos_client.Apisappsv1beta1Api()
        api_response = api_instance.list_namespaced_application_instance(tenant_name)

        if instance_name is None:
            logger.warning("Deleting all instances of tenant {}".format(tenant_name))

        for i, item in enumerate(api_response.items):
            metaname = item.metadata.name
            if instance_name is None or metaname.startswith(instance_name):
                api_response = api_instance.delete_namespaced_application_instance('', tenant_name, metaname,
                                                                                   grace_period_seconds=0)
                logger.info("Deleting instance {} of tenant {}: {}".format(
                    metaname, tenant_name, self._pprint_instance_removal_rsp(api_response)))

    @handle_tos_errors
    def get_instances(self, tenant_name, instance_name=None):
        """
        Get all instances of specific tenant
        :param tenant_name: the name of tenant
        :param instance_name: the name of instance
        :return: a list of instance objects
        """
        api_instance = tos_client.Apisappsv1beta1Api()

        if instance_name is None:
            instances_response = api_instance.list_namespaced_application_instance(tenant_name)
            instances = []
            for item in instances_response.items:
                instances.append(InstanceObject(item))
            return instances
        else:
            instance_response = api_instance.read_namespaced_application_instance(tenant_name, instance_name)
            return InstanceObject(instance_response)

    @handle_tos_errors
    def get_raw_instances(self, tenant_name, instance_name=None, **kwargs):
        api_instance = tos_client.Apisappsv1beta1Api()
        if instance_name:
            return api_instance.read_namespaced_application_instance(tenant_name, instance_name)
        else:
            return api_instance.list_namespaced_application_instance(tenant_name, **kwargs)

    @handle_tos_errors
    def get_detailed_instances(self, tenant_name, instance_name=None):
        """
        Get all instances of specific tenant with detailed info
        :param tenant_name: the name of tenant
        :param instance_name: the name of instance
        :return: a list of instance objects
        """
        api_instance = tos_client.Apisappsv1beta1Api()
        instances_response = api_instance.list_namespaced_application_instance(tenant_name)

        instances = []
        for item in instances_response.items:
            instance = InstanceObject(item)
            if instance_name and instance.instance_name != instance_name:
                continue
            label_selector = '%s=%s' % (self.label_control_prefix, instance.instance_id)
            instance.pods.extend(self.get_instance_pods(tenant_name, label_selector=label_selector))
            instance.services.extend(self.get_instance_services(tenant_name, label_selector=label_selector))
            instance.stateful_sets.extend(self.get_instance_stateful_sets(tenant_name, label_selector=label_selector))
            instance.deployments.extend(self.get_instance_deployments(tenant_name, label_selector=label_selector))
            instances.append(instance)
        return instances

    @handle_tos_errors
    def get_instance_services(self, tenant_name, **kwargs):
        """
        Get all services associated with an instance
        :param tenant_name: the name of tenant
        :param kwargs: arguments to specify label selector
        :return: a list of service objects
        """
        api_instance = tos_client.Apiv1Api()
        services_objs = api_instance.list_namespaced_service(tenant_name, **kwargs)

        services = []
        for item in services_objs.items:
            services.append(ServiceObject(item))
        return services

    @handle_tos_errors
    def get_instance_pods(self, tenant_name, pod_name=None, **kwargs):
        """
        Get all pods associated with an instance
        :param tenant_name: the name of tenant
        :param kwargs: arguments to specify label selector
        :return: a list of pod objects
        """
        api_instance = tos_client.Apiv1Api()

        if pod_name is None:
            pods_objs = api_instance.list_namespaced_pod(tenant_name, **kwargs)

            pods = []
            for item in pods_objs.items:
                pod = PodObject(item)
                container_statuses = item.status.container_statuses
                if item.status.container_statuses is not None:
                    for cs in container_statuses:
                        if cs.ready is not True:
                            pod.is_ready = False
                            break
                conditions = item.status.conditions
                if conditions is not None and len(conditions) > 0:
                    pod.reason = conditions[0].reason

                pods.append(pod)
            return pods
        else:
            pod_obj = api_instance.read_namespaced_pod(tenant_name, pod_name)
            return PodObject(pod_obj)

    @handle_tos_errors
    def delete_instance_pvcs(self, tenant_name, instance_ids=None):
        """
        Delete all the pvcs associated with a list of instances
        :param tenant_name: the name of tenant
        :param instance_ids: a list of instance_id
        :return: None
        """
        api_instance = tos_client.Apiv1Api()

        if instance_ids:
            for instance_id in instance_ids:
                label_selector = '%s=%s' % (self.label_control_prefix, instance_id)
                api_response = api_instance.deletecollection_namespaced_persistent_volume_claim(
                    tenant_name, label_selector=label_selector)
                logger.info("Deleting pvcs of instance {}: {}".format(
                    instance_id, self._pprint_instance_removal_rsp(api_response)))
        else:
            api_response = api_instance.deletecollection_namespaced_persistent_volume_claim(tenant_name)
            logger.info("Deleting pvs {}".format(self._pprint_instance_removal_rsp(api_response)))

    def get_instance_stateful_sets(self, tenant_name, **kwargs):
        """
        Get a list of StatefulSetObject instances
        :param tenant_name: the name of tenant
        :param instance_id: instance id
        :return: a list of StatefulSetObject instances
        """
        api_instance = tos_client.Apisappsv1beta1Api()
        stateful_sets = api_instance.list_namespaced_stateful_set(tenant_name, **kwargs)

        stateful_set_objs = []
        for stateful_set in stateful_sets.items:
            stateful_set_obj = StatefulSetObject(stateful_set)
            stateful_set_objs.append(stateful_set_obj)

        return stateful_set_objs

    @handle_tos_errors
    def get_instance_deployments(self, tenant_name, **kwargs):
        """
        Get a list of DeploymentObject Instance
        :param tenant_name: the name of tenant
        :param instance_id: instance id
        :return: a list of DeploymentObject instances
        """
        api_instance = tos_client.Apisextensionsv1beta1Api()
        deployments = api_instance.list_namespaced_deployment(tenant_name, **kwargs)

        deployment_objs = []
        for deployment in deployments.items:
            deployment_obj = DeploymentObject(deployment)
            deployment_objs.append(deployment_obj)

        return deployment_objs

    @handle_tos_errors
    def patch_instance(self, tenant_name, instance_name, update_patch):
        api_instance = tos_client.Apisappsv1beta1Api()
        api_response = api_instance.patch_namespaced_application_instance(update_patch,
                                                                          namespace=tenant_name,
                                                                          name=instance_name)
        logger.info("Partially updating instance {} of tenant {}: {}".format(
            instance_name, tenant_name, self._pprint_instance_patch_rsp(api_response)))


class KubePodOp(KubeOp):
    """
    Operator to get pod info
    """
    def __init__(self):
        super(KubePodOp, self).__init__()

    @handle_tos_errors
    def get_raw_pods(self, tenant_name, pod_name=None, **kwargs):
        api_pod = tos_client.Apiv1Api()
        if pod_name:
            return api_pod.read_namespaced_pod(tenant_name, pod_name)
        else:
            return api_pod.list_namespaced_pod(tenant_name, **kwargs)

    @handle_tos_errors
    def get_pod_events(self, tenant_name, pod_name=None, **kwargs):
        """
        Get a list of Event instances belonging to the specific pod/all the pods of the tenant
        :param tenant_name: the name of tenant
        :param pod_name: the name of pod
        :param kwargs:
        :return: a list of Event instances
        """
        api_pod = tos_client.Apiv1Api()
        if pod_name:
            field_selector = '%s=%s' % ('involvedObject.name', pod_name)
            event_objs = api_pod.list_namespaced_event(tenant_name, field_selector=field_selector, **kwargs)
        else:
            event_objs = api_pod.list_namespaced_event(tenant_name, **kwargs)

        events = []
        for event_obj in event_objs.items:
            if event_obj.involved_object.kind == 'Pod':
                events.append(EventObject(event_obj))

        return events

    @handle_tos_errors
    def get_pod_log(self, tenant_name, pod_name, container_name=None, **kwargs):
        """
        Get log of the specific pod
        :param tenant_name: the name of tenant
        :param pod_name: the name of pod
        :param kwargs:
        :return: string
        """
        api_pod = tos_client.Apiv1Api()
        if container_name is None:
            return api_pod.read_namespaced_pod_log(tenant_name, pod_name, tail_lines=1000, **kwargs)
        else:
            return api_pod.read_namespaced_pod_log(tenant_name, pod_name, container=container_name,
                                                   tail_lines=1000, **kwargs)


class KubeNodeOp(KubeOp):
    """
    Operator to get node info
    """

    def __init__(self):
        super(KubeNodeOp, self).__init__()

    @handle_tos_errors
    def get_nodes(self):
        """
        Get all nodes
        :return: a list of node objects
        """
        api_node = tos_client.Apiv1Api()
        nodes_objs = api_node.list_node()

        nodes = []
        for item in nodes_objs.items:
            node = NodeObject(item)
            nodes.append(node)

        return nodes
