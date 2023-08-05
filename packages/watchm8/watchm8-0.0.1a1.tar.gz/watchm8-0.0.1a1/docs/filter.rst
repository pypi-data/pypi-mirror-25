Filter
======

Filters are expressed in a single Python expression. Python expressions are
extended in that regard, that you can navigate structured data (dict/map) like
a native Python object. Using globals like `len()`, `list()` etc. is not
allowed. You can access methods provided by native data types like str, int,
float etc.

Accessible by the filter are 2 objects:

* Event
* Emitter

Event
-----

The event is produced by :doc:`/watchers` is a simple Python object looking like
this:

.. autoclass:: watchm8.event.Event
  :members:

Emitter
-------

The emitter is in almost all cases the Watcher, which produced the event. If
an action was used to emit a new event the action would be the emitter.


Examples
--------

.. code-block:: python

  event.type == "created" and event.data.metadata.labels.environment == "dev"

.. code-block:: python

  event.type.startswith("created") and event.data.metadata.labels.has_key("environment")
