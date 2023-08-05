Introduction
============

The idea behind `Watchm8` is to watch the state of resources, filter events
produced by changes in state and execute actions. It's especially designed
to automate and integrate Kubernetes, the container orchestration tool.

.. code-block:: yaml

  jobs:
    - watch:
        kind: .k8s.ConfigMap
        namespace: default
        label_selector: project=myservice
      filter: event.type == "created" and event.data.metadata.labels.environment == "prod"
      do:
        kind: .k8s.CreateUpdateDeployment
        yaml_file: '/path/to/deployment.yaml'
        is_template: true

Job
---

Individual workflows are expressed in `jobs`. Each job receives events through
one or more :doc:`/watchers`, :doc:`/filter` data and triggers one or more
:doc:`/actions` if events matched the filter.

In this example state changes in Kubernetes for ConfigMaps in the default
namespace labeled `project=myservice` are watched, and will trigger a
create/update of a deployment if the event matches the type `created` and is
labeled `environment: prod`.

Applications:

* Reload services on config changes
* Deploy resources along with others (ex. based on annotations)
* Deploy stack in multi-tenant application environment
* Integrate external config store with K8s ConfigMaps
* Monitoring
* ...
