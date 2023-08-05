Installation
============

Using pip
---------

To install the most recent stable release of the library, use `pip`_:

.. code-block:: console

    $ pip install streamsets

.. _pip: https://pip.pypa.io


.. _activation:

Activation
----------

After installing for the first time, the library requires
an activation key to be used. This key should be placed in the user configuration
directory under ``<user home folder>/.streamsets`` in a folder called
``activation``. If not present the first time the library is imported, this
directory will be created for you automatically. If this key is not in place, a
:py:exc:`streamsets.exceptions.ActivationError`
will be raised whenever you attempt to create an instance of
:py:class:`streamsets.DataCollector`:

.. code-block:: python

    >>> from streamsets import *
    >>> data_collector = DataCollector('http://localhost:18630')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<site package directory>/streamsets/sdc.py", line 50, in __init__
        password=self.password)
      File "streamsets/sdc_api.pyx", line 71, in streamsets.sdc_api.ApiClient.__init__
      File "streamsets/sdc_api.pyx", line 76, in streamsets.sdc_api.ApiClient._verify_activation
    streamsets.exceptions.ActivationError: Failed to activate Python SDK for StreamSets (reason: Could not find activation file at <user home folder>/.streamsets/activation/rsa-signed-activation-info.properties).

If you have an ``rsa-signed-activation-info.properties`` file, simply place it into the directory
referenced above and retry your command. If you don't yet have this file, contact StreamSets with
a request for access to the Python SDK.
