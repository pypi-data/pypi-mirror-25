.. module:: streamsets

Usage instructions
==================

The examples below assume you've installed the ``streamsets`` library
and are inside a Python 3.4+ interpreter.


Creating a pipeline
-------------------

Use of the Python SDK begins by importing the library. For convenience, doing a
wildcard import will give you direct access to the :py:class:`DataCollector` class:

.. code-block:: python

    >>> from streamsets import *

Next, create an instance of :py:class:`DataCollector`, passing in, at a minimum,
the URL of your StreamSets Data Collector instance (including the port):

.. code-block:: python

    >>> data_collector = DataCollector('http://localhost:18630')

Assuming you've :ref:`activated the library <activation>`, you can now get an
instance of :py:class:`PipelineBuilder`:

.. code-block:: python

    >>> builder = data_collector.get_pipeline_builder()

We get :py:class:`Stage` instances from this builder by calling :py:meth:`PipelineBuilder.add_stage`.
See the API reference for this method for details on the arguments it takes.

As shown in the :ref:`first example <first-example>`, the simplest type of pipeline
directs one origin into one destination. For this example, we do this with ``Dev Raw Data Source``
origin and ``Trash`` destination, respectively:

.. code-block:: python

    >>> dev_raw_data_source = builder.add_stage('Dev Raw Data Source')
    >>> trash = builder.add_stage('Trash')

With :py:class:`Stage` instances in hand, we can connect them by using the ``>>`` operator,
and then building a :py:class:`Pipeline` instance with the :py:meth:`PipelineBuilder.build` method:

.. code-block:: python

    >>> dev_raw_data_source >> trash
    >>> pipeline = builder.build('My first pipeline')

Finally, to add this pipeline to your Data Collector instance, pass it to the
:py:meth:`DataCollector.add_pipeline` method:

.. code-block:: python

    >>> data_collector.add_pipeline(pipeline)


Configuring stages
------------------

In practice, it's rare to have stages in your pipeline that haven't had some configurations
changed from their default values. When using the Python SDK, the names to use when referring
to these configurations can be inferred from the StreamSets Data Collector UI (e.g.
``Data Format`` becomes ``data_format``) or by using Python's built-in :py:meth:`help` method
on an instance of :py:class:`Stage`:

.. code-block:: python

    >>> help(dev_raw_data_source)

.. image:: _static/dev_raw_data_source_help.png

With the attribute name in hand, you can read the value of the configuration:

.. code-block:: python

    >>> dev_raw_data_source.max_line_length
    1024

As for setting the value of the configuration, this can be done in one of two ways
depending on your use case:


Single configurations
~~~~~~~~~~~~~~~~~~~~~

If you only have one or two configurations to update, you can set them using attributes of the
:py:class:`Stage` instance. Continuing in the vein of our example:

.. code-block:: python

    >>> dev_raw_data_source.data_format = 'TEXT'
    >>> dev_raw_data_source.raw_data = 'hi\nhello\nhow are you?'

Multiple configurations
~~~~~~~~~~~~~~~~~~~~~~~

For readability, it's sometimes better to set all attributes simultaneously with
one call to the :py:meth:`Stage.set_attributes` method:

.. code-block:: python

    >>> dev_raw_data_source.set_attributes(data_format='TEXT',
                                           raw_data='hi\nhello\nhow are you?')

Connecting stages
-----------------

As described above, to connect the output of one stage to the input of
another, simply use the ``>>`` operator between two :py:class:`Stage` instances:

.. code-block:: python

    >>> dev_raw_data_source >> trash

For stages with multiple outputs, simply use ``>>`` multiple times:

.. code-block:: python

    >>> file_tail = builder.add_stage('File Tail')
    >>> file_tail >> trash_1
    >>> file_tail >> trash_2

.. image:: _static/file_tail_to_two_trashes.png

It is also possible to connect the output of one stage to the inputs of multiple
stages, as in the image below:

.. image:: _static/dev_data_generator_to_two_trashes.png

To do this, put the :py:class:`Stage` instances to which you'll be connecting the same
output into a list before using the ``>>`` operator:

.. code-block:: python

    >>> trash_1 = builder.add_stage('Trash')
    >>> trash_2 = builder.add_stage('Trash')
    >>> dev_raw_data_source >> [trash_1, trash_2]


Events
------

To connect the event lane of one stage to another, use the ``>=`` operator:

.. code-block:: python

    >>> dev_data_generator >> trash_1
    >>> dev_data_generator >= trash_2

.. image:: _static/dev_data_generator_with_events.png


Error stages
------------

To add an error stage, use :py:meth:`streamsets.PipelineBuilder.add_error_stage`:

.. code-block:: python

    >>> discard = builder.add_error_stage('Discard')
