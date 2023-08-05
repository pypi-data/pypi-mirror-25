.. readme-start

StreamSets SDK for Python
=========================

The StreamSets SDK for Python is a library
that helps users create data pipelines programmatically in Python 3.4+. It can generate and
import a functional (albeit trivial) pipeline in less than 10 lines of code:

.. code-block:: python

    from streamsets import *
    server_url = 'http://localhost:18630'
    data_collector = DataCollector(server_url)

    builder = data_collector.get_pipeline_builder()
    dev_data_generator = builder.add_stage('Dev Data Generator')
    trash = builder.add_stage('Trash')

    dev_data_generator >> trash  # connect the Dev Data Generator origin to the Trash destination.

    pipeline = builder.build('My first pipeline')
    data_collector.add_pipeline(pipeline)

The resulting pipeline can be examined by opening the SDC user interface
and selecting the ``My first pipeline`` pipeline:

.. readme-end

.. image:: docs/_static/dev_data_generator_to_trash.png
    :width: 75%
