import pytest
from watchm8.factories.watcher import watcher_factory
from watchm8.factories.job import job_factory
from watchm8.factories.action import action_factory
from watchm8.factories.dispatcher import dispatcher_factory


def test_dispatcher_factory():
    from watchm8.factories.dispatcher import DEFAULT
    from watchm8.dispatchers.core import Sequential

    d = dispatcher_factory({
        'kind': '.core.Sequential'
    }, [])
    assert type(d) is Sequential

    d = dispatcher_factory(None, [])
    assert type(d) is DEFAULT


def test_action_factory():
    from watchm8.actions.say import Event
    a = action_factory({
        'kind': '.say.Event'
    })

    assert type(a) is Event

    with pytest.raises(KeyError):
        action_factory({})


def test_watcher_factory():
    from watchm8.watchers.k8s import Pod

    w = watcher_factory({
        'kind': '.k8s.Pod',
        'namespace': 'spark',
        'label_selector': 'name=web-ui',
        'config': {
            'type': 'kube_config'
        }
    })

    assert type(w) is Pod

    with pytest.raises(KeyError):
        watcher_factory({})

    with pytest.raises(KeyError):
        watcher_factory({
            'namespace': 'spark',
            'label_selector': 'name=web-ui',
            'config': {
                'type': 'kube_config'
            }
        })


def test_job_factory():
    from watchm8.job import Job

    j = job_factory({
        'watch': {
            'kind': '.k8s.Pod',
            'namespace': 'spark',
            'label_selector': 'name=web-ui',
            'config': {'type': 'kube_config'}
        },
        'filter': 'metadata.annotations.gelf == "true"',
        'do': {'kind': '.say.Event'}
    })
    assert type(j) is Job

    job_factory({
        'watch': [{
            'kind': '.k8s.Pod',
            'namespace': 'spark',
            'label_selector': 'name=web-ui',
            'config': {'type': 'kube_config'}
        }],
        'filter': 'metadata.annotations.gelf == "true"',
        'dispatcher': {
            'kind': '.core.Sequential',
        },
        'do': [{'kind': '.say.Event'}]
    })
    assert type(j) is Job
