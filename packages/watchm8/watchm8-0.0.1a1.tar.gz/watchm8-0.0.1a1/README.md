# Watchm8

Event driven *If This Then That* like automation tool for watchable resources.

**WARNING: Alpha stage, under heavy development**

![Watchm8 Architecture](/docs/_static/Watchm8.png?raw=true "Watchm8 Architecture")

## Intro

The idea behind `Watchm8` is to watch the state of resources, filter events
produced by changes in state and execute actions. It's especially designed
to automate and integrate Kubernetes, the container orchestration tool.

```
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
```

Individual workflows are expressed in `jobs`. Each job receives events through
n `watchers`, filters data and triggers n `actions` if events matched the filter.

In this example state changes in Kubernetes for ConfigMaps in the default namespace
labeled `project=myservice` are watched, and will trigger a create/update of a deployment
if the event matches the type `created` and is labeled `environment: prod`.

Applications:

* Reload services on config changes
* Deploy resources along with others (ex. based on annotations)
* Deploy stack in multi-tenant application environment
* Integrate external config store with K8s ConfigMaps
* Monitoring
* ...

## Motivation

Good system architectures are a matter of how well different parts of your
stack are integrated with each other. Introducing tech like containers, CI/CD,
clusters and a hole bunch of helper and managing tools in your infrastructure
almost always requires you to integrate new tech with old tech, or old
workflow with new workflow. You end up writing glue code. Watchm8 is here to
help you with integrating and automating new tech with old tech,
or tool A with tool B, or whatever workflow you can come up with.

## Author

* Simon Pirschel
* https://aboutsimon.com/

## License

*Apache License, Version 2.0*
