# -*- coding: utf-8 -*-

from urllib3.response import ReadTimeoutError
from kubernetes import client, watch
from kubernetes.config import load_incluster_config, load_kube_config
from ._base import BaseWatcher
from ..event import Event


# TODO: config loader per Watcher


'''
.. module:: k8s
   :synopsis: Kubernetes watchers

.. moduleauthor:: Simon Pirschel <simon@aboutsimon.com>
'''


class K8sWatcher(BaseWatcher):

    def __init__(self, config=None, namespace=None, label_selector=None):
        BaseWatcher.__init__(self)

        load_kube_config()

        self._namespace = namespace
        self._label_selector = label_selector

    @property
    def _stream_func(self):
        raise NotImplementedError()

    @property
    def _stream_kwargs(self):
        kwargs = {'label_selector': self._label_selector}
        if self._namespace is not None:
            kwargs['namespace'] = self._namespace

        return kwargs

    def _run(self):
        w = watch.Watch()
        last_version = 0
        kwargs = self._stream_kwargs
        kwargs['_request_timeout'] = 5

        while self._stop_watcher is False:
            kwargs['resource_version'] = last_version

            try:
                for event in w.stream(self._stream_func, **kwargs):
                    self._emit(Event(event['type'], event['raw_object']))
                    version = int(
                        event['raw_object']['metadata']['resourceVersion']
                    )
                    if version > last_version:
                        last_version = version

                    if self._stop_watcher is True:
                        w.stop()
                        break
            except ReadTimeoutError:
                continue


class Pod(K8sWatcher):

    '''Observe Pod objects in a Kubernetes cluster

    Example:
        .. code-block:: yaml

            watch:
                kind: .k8s.Pod

    Args:
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
        namespace (str, optional): Observe objects only in given namespace
        label_selector (str, optional): Select objects based on given label
            selector, eg: environment=prod,app=web
    '''

    @property
    def _stream_func(self):
        api = client.CoreV1Api()
        func = api.list_pod_for_all_namespaces

        if self._namespace is not None:
            func = api.list_namespaced_pod

        return func


class Service(K8sWatcher):

    '''Observe Service objects in a Kubernetes cluster

    Example:
        .. code-block:: yaml

            watch:
                kind: .k8s.Service

    Args:
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
        namespace (str, optional): Observe objects only in given namespace
        label_selector (str, optional): Select objects based on given label
            selector, eg: environment=prod,app=web
    '''

    @property
    def _stream_func(self):
        api = client.CoreV1Api()
        func = api.list_service_for_all_namespaces

        if self._namespace is not None:
            func = api.list_namespaced_service

        return func


class ConfigMap(K8sWatcher):

    '''Observe ConfigMap objects in a Kubernetes cluster

    Example:
        .. code-block:: yaml

            watch:
                kind: .k8s.ConfigMap

    Args:
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
        namespace (str, optional): Observe objects only in given namespace
        label_selector (str, optional): Select objects based on given label
            selector, eg: environment=prod,app=web
    '''

    @property
    def _stream_func(self):
        api = client.CoreV1Api()
        func = api.list_config_map_for_all_namespaces

        if self._namespace is not None:
            func = api.list_namespaced_config_map

        return func


class Node(K8sWatcher):

    '''Observe Node objects in a Kubernetes cluster

    Example:
        .. code-block:: yaml

            watch:
                kind: .k8s.Node

    Args:
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
        namespace (str, optional): Observe objects only in given namespace
        label_selector (str, optional): Select objects based on given label
            selector, eg: environment=prod,app=web
    '''

    @property
    def _stream_func(self):
        api = client.CoreV1Api()
        func = api.list_node_for_all_namespaces

        if self._namespace is not None:
            func = api.list_namespaced_node

        return func


class Namespace(K8sWatcher):

    '''Observe Namespace objects in a Kubernetes cluster

    Example:
        .. code-block:: yaml

            watch:
                kind: .k8s.Namespace

    Args:
        config (dict, optional): Kubernetes API auth configuration, defaults
            to using ~/.kube/config
        label_selector (str, optional): Select objects based on given label
            selector, eg: environment=prod,app=web
    '''

    @property
    def _stream_func(self):
        api = client.CoreV1Api()
        return api.list_namespace

    @property
    def _stream_kwargs(self):
        return {'label_selector': self._label_selector}
