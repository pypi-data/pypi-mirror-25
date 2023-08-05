.. _api:

API Reference
=============

.. module:: streamsets

StreamSets Data Collector
-------------------------
Constructs to interact with StreamSets Data Collector instances.

.. autoclass:: DataCollector
    :members:

.. autoattribute:: sdc.DEFAULT_SDC_USERNAME
.. autoattribute:: sdc.DEFAULT_SDC_PASSWORD


Pipelines
---------
Abstractions to create or examine pipelines.

.. autoclass:: PipelineBuilder
    :members:
.. autoclass:: Pipeline
    :members:
.. autoclass:: Stage
    :members:
.. autoclass:: Configuration
    :members:
.. autoclass:: DataRule
    :members:
.. autoclass:: DataDriftRule
    :members:

Exceptions
----------

.. automodule:: streamsets.exceptions
    :members:
