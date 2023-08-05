# -*- coding: utf-8 -*-

from jinja2 import Template
from kubernetes import client
from kubernetes.config import load_kube_config  # , load_incluster_config
from yaml import load
from ._base import BaseAction, JobFailed


# TODO: config loader per Watcher

'''
.. module:: k8s
   :synopsis: Kubernetes actions

.. moduleauthor:: Simon Pirschel <simon@aboutsimon.com>
'''


class CreateUpdateResource(BaseAction):

    '''Base class for all create/update actions

    Args:
        yaml_file (str): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = None

    def __init__(self, yaml_file, namespace='default', is_template=False,
                 raise_on_failure=True, config=None):
        self._yaml_file = yaml_file
        self._namespace = namespace
        self._is_template = is_template
        self._raise_on_failure = raise_on_failure
        self._config = config

        load_kube_config()

        self._api = self._get_api()

    def _get_api(self):
        raise NotImplementedError()

    def _read_resource(self, name):
        raise NotImplementedError()

    def _update_resource(self, name, body):
        raise NotImplementedError()

    def _create_resource(self, body):
        raise NotImplementedError()

    def __call__(self, event, emitter):
        with open(self._yaml_file, 'r') as fh:
            content = fh.read()

        if self._is_template is True:
            content = Template(content)\
                .render(event=event, emitter=emitter)

        body = load(content)
        name = body['metadata']['name']
        patch = False

        try:
            self._read_resource(name)
            patch = True
        except client.rest.ApiException as e:
            if e.status == 404:
                patch = False
            else:
                if self._raise_on_failure is True:
                    raise JobFailed(
                        'Could not get %s %s. %s' %
                        (self.RESOURCE_NAME, name, str(e))
                    )

        if patch is True:
            try:
                self._update_resource(name, body)
            except client.rest.ApiException as e:
                if self._raise_on_failure is True:
                    raise JobFailed(
                        'Could not update %s %s. %s' %
                        (self.RESOURCE_NAME, name, str(e))
                    )
        else:
            try:
                self._create_resource(body)
            except client.rest.ApiException as e:
                if self._raise_on_failure is True:
                    raise JobFailed(
                        'Could not create %s %s. %s' %
                        (self.RESOURCE_NAME, name, str(e))
                    )


class DeleteResource(BaseAction):

    '''Base class for all delete actions

    Args:
        name (str, optional): Name of Kuberntes resource
        yaml_file (str, optional): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = None

    def __init__(self, name=None, yaml_file=None, namespace='default',
                 is_template=False, raise_on_failure=True, config=None):
        self._name = name
        self._yaml_file = yaml_file
        self._namespace = namespace
        self._is_template = is_template
        self._raise_on_failure = raise_on_failure
        self._config = config

        load_kube_config()

        self._api = self._get_api()

        if name is None and yaml_file is None:
            raise ValueError('name or yaml_file must be specified')

        if name and yaml_file:
            raise ValueError('name or yaml_file must be specified, not both')

        if name is None:
            with open(self._yaml_file, 'r') as fh:
                content = fh.read()
                body = load(content)
                self._name = body['metadata']['name']

    def _get_api(self):
        raise NotImplementedError()

    def _read_resource(self, name):
        raise NotImplementedError()

    def _delete_resource(self, name):
        raise NotImplementedError()

    def __call__(self, event, emitter):
        try:
            self._delete_resource(self._name)
        except client.rest.ApiException as e:
            if self._raise_on_failure is True:
                raise JobFailed(
                    'Could not delete %s %s. %s' %
                    (self.RESOURCE_NAME, self._name, str(e))
                )


class CreateUpdateService(CreateUpdateResource):

    '''Create or update Kubernetes service

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.CreateUpdateService
                yaml_file: /path/to/service.yaml
                namespace: default
                is_template: False

    Args:
        yaml_file (str): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'service'

    def __init__(self, yaml_file, namespace='default', is_template=False,
                 raise_on_failure=True):
        CreateUpdateResource.__init__(
            self, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.CoreV1Api()

    def _read_resource(self, name):
        return self._api.read_namespaced_service(name, self._namespace)

    def _update_resource(self, name, body):
        return self._api.patch_namespaced_service(
            name, namespace=self._namespace, body=body
        )

    def _create_resource(self, body):
        return self._api.create_namespaced_service(
            body=body, namespace=self._namespace
        )


class DeleteService(DeleteResource):

    '''Delete Kubernetes Service

    The resource name needs to be specified directly through ``name`` or
    through the `name` attribute in ``yaml_file``.

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.DeleteService
                name: myresource
                namespace: default
                is_template: False

    Args:
        name (str, optional): Name of Kuberntes resource
        yaml_file (str, optional): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'service'

    def __init__(self, name=None, yaml_file=None, namespace='default',
                 is_template=False, raise_on_failure=True):
        DeleteResource.__init__(
            self, name, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.CoreV1Api()

    def _delete_resource(self, name):
        return self._api.delete_namespaced_service(
            name=name, namespace=self._namespace, body=client.V1DeleteOptions()
        )


class CreateUpdatePod(CreateUpdateResource):

    '''Create or update Kubernetes Pod

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.CreateUpdatePod
                yaml_file: /path/to/pod.yaml
                namespace: default
                is_template: False

    Args:
        yaml_file (str): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'pod'

    def __init__(self, yaml_file, namespace='default', is_template=False,
                 raise_on_failure=True):
        CreateUpdateResource.__init__(
            self, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.CoreV1Api()

    def _read_resource(self, name):
        return self._api.read_namespaced_pod(name, self._namespace)

    def _update_resource(self, name, body):
        return self._api.patch_namespaced_pod(
            name, namespace=self._namespace, body=body
        )

    def _create_resource(self, body):
        return self._api.create_namespaced_pod(
            body=body, namespace=self._namespace
        )


class DeletePod(DeleteResource):

    '''Delete Kubernetes Pod

    The resource name needs to be specified directly through ``name`` or
    through the `name` attribute in ``yaml_file``.

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.DeletePod
                name: myresource
                namespace: default
                is_template: False

    Args:
        name (str, optional): Name of Kuberntes resource
        yaml_file (str, optional): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'pod'

    def __init__(self, name=None, yaml_file=None, namespace='default',
                 is_template=False, raise_on_failure=True):
        DeleteResource.__init__(
            self, name, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.CoreV1Api()

    def _delete_resource(self, name):
        return self._api.delete_namespaced_pod(
            name=name, namespace=self._namespace, body=client.V1DeleteOptions()
        )


class CreateUpdateConfigMap(CreateUpdateResource):

    '''Create or update Kubernetes ConfigMap

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.CreateUpdateConfigMap
                yaml_file: /path/to/config_map.yaml
                namespace: default
                is_template: False

    Args:
        yaml_file (str): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'config_map'

    def __init__(self, yaml_file, namespace='default', is_template=False,
                 raise_on_failure=True):
        CreateUpdateResource.__init__(
            self, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.CoreV1Api()

    def _read_resource(self, name):
        return self._api.read_namespaced_config_map(name, self._namespace)

    def _update_resource(self, name, body):
        return self._api.patch_namespaced_config_map(
            name, namespace=self._namespace, body=body
        )

    def _create_resource(self, body):
        return self._api.create_namespaced_config_map(
            body=body, namespace=self._namespace
        )


class DeleteConfigMap(DeleteResource):

    '''Delete Kubernetes ConfigMap

    The resource name needs to be specified directly through ``name`` or
    through the `name` attribute in ``yaml_file``.

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.DeleteConfigMap
                name: myresource
                namespace: default
                is_template: False

    Args:
        name (str, optional): Name of Kuberntes resource
        yaml_file (str, optional): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'config_map'

    def __init__(self, name=None, yaml_file=None, namespace='default',
                 is_template=False, raise_on_failure=True):
        DeleteResource.__init__(
            self, name, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.CoreV1Api()

    def _delete_resource(self, name):
        return self._api.delete_namespaced_config_map(
            name=name, namespace=self._namespace, body=client.V1DeleteOptions()
        )


class CreateUpdateDeployment(CreateUpdateResource):

    '''Create or update Kubernetes Deployment

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.CreateUpdateDeployment
                yaml_file: /path/to/deployment.yaml
                namespace: default
                is_template: False

    Args:
        yaml_file (str): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'deployment'

    def __init__(self, yaml_file, namespace='default', is_template=False,
                 raise_on_failure=True):
        CreateUpdateResource.__init__(
            self, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.AppsV1beta1Api()

    def _read_resource(self, name):
        return self._api.read_namespaced_deployment(name, self._namespace)

    def _update_resource(self, name, body):
        return self._api.patch_namespaced_deployment(
            name, namespace=self._namespace, body=body
        )

    def _create_resource(self, body):
        return self._api.create_namespaced_deployment(
            body=body, namespace=self._namespace
        )


class DeleteDeployment(DeleteResource):

    '''Delete Kubernetes Deployment

    The resource name needs to be specified directly through ``name`` or
    through the `name` attribute in ``yaml_file``.

    Example:
        .. code-block:: yaml

            do:
                kind: .k8s.DeleteDeployment
                name: myresource
                namespace: default
                is_template: False

    Args:
        name (str, optional): Name of Kuberntes resource
        yaml_file (str, optional): Path to YAML resource definition
        namespace (str): Kubernetes namespace, default: 'default'
        is_template (bool): `yaml_file` is template and needs to be rendered
            before deserialization, default: False
        raise_on_failure (bool): Raise exception if action failed, default: True
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
    '''

    RESOURCE_NAME = 'deployment'

    def __init__(self, name=None, yaml_file=None, namespace='default',
                 is_template=False, raise_on_failure=True):
        DeleteResource.__init__(
            self, name, yaml_file, namespace, is_template, raise_on_failure
        )

    def _get_api(self):
        return client.AppsV1beta1Api()

    def _delete_resource(self, name):
        return self._api.delete_namespaced_deployment(
            name=name, namespace=self._namespace, body=client.V1DeleteOptions()
        )
