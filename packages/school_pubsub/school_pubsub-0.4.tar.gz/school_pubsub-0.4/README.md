# PubSubGuru

Simple Publish Subscribe python library

[![PyPI version](https://badge.fury.io/py/school_pubsub.svg)](https://badge.fury.io/py/school_pubsub)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d52688e6b2e940689f592c15f67a8879)](https://www.codacy.com/app/toast38coza/PubSubGuru?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AppointmentGuru/PubSubGuru&amp;utm_campaign=Badge_Grade)

[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/d52688e6b2e940689f592c15f67a8879)](https://www.codacy.com/app/toast38coza/PubSubGuru?utm_source=github.com&utm_medium=referral&utm_content=AppointmentGuru/PubSubGuru&utm_campaign=Badge_Coverage)

### Installation

```
pip install school_pubsub
```

### Backends available

* PubNub
* MockBackend (coming soon)
* Pika (RabbitMQ) (coming soon)
* Celery (coming soon)

### Gettings started

**Example usage**

**Publish**

```
pubsub = get_backend('backends', 'PubNubBackend', 'some-channel')
key = 'myapp.did_something'
payload: {"foo": "bar"}
pubsub.publish(key, payload)
```

**Subscribe**

```
"""
listen's for all events on 'some-channel', will only execute events which have a key
that matches in functionmapper. e.g.: `myapp.didsomething`

e.g.: an event like above. e.g.::

{ key: "myapp.didsomething",
  payload: {"foo": "bar"}
}

Would result in the subscriber calling: `thisapp.tasks.handle_did_something(payload)`
"""

functionmapper = {
    "myapp.didsomething": {
        "module": "thisapp.tasks",
        "method": "handle_did_something"
    }
}
pubsub = get_backend('backends', 'PubNubBackend', 'some-channel')

# this is a run_forever, you'll want to run it as it's own process
pubsub.subscribe(functionmapper)

```

### Packaging:

```python setup.py sdist upload```
