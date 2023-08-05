# Copyright 2017 StreamSets Inc.

"""Abstractions for interacting with StreamSets Data Collector."""

import logging
from urllib.parse import urlparse

from . import sdc_api, sdc_models

logger = logging.getLogger(__name__)

# The `#:` constructs at the end of assignments are part of Sphinx's autodoc functionality.
DEFAULT_SDC_USERNAME = 'admin'  #:
DEFAULT_SDC_PASSWORD = 'admin'  #:


class DataCollector:
    """Class to interact with StreamSets Data Collector.

    Args:
        server_url (:obj:`str`): URL of an existing SDC deployment with which to interact. If
            not set, the Test Framework will manage a Docker-based Data Collector instance.
            Default: ``None``
        username (:obj:`str`): SDC username. This is used when interacting with the SDC REST API,
            and the user must already exist. Default: :py:const:`sdc.DEFAULT_SDC_USERNAME`
        password (:obj:`str`): SDC password. Default: :py:const:`sdc.DEFAULT_SDC_PASSWORD`
    """
    def __init__(self,
                 server_url,
                 username=None,
                 password=None,
                 **kwargs):
        self.server_url = server_url
        self.username = username or DEFAULT_SDC_USERNAME
        self.password = password or DEFAULT_SDC_PASSWORD

        self.api_client = sdc_api.ApiClient(server_url=self.server_url,
                                            username=self.username,
                                            password=self.password,
                                            **kwargs)

        # Keep track of the server_host so that tests that may need it (e.g. to set configurations) can use it.
        self.server_host = urlparse(self.server_url).netloc.split(':')[0]

        self._stage_definitions = None

    def add_pipeline(self, *pipelines):
        """Add one or more pipelines to the DataCollector instance.

        Args:
            *pipelines: One or more instances of :py:class:`streamsets.Pipeline`
        """
        for pipeline in set(pipelines):
            logger.info('Importing pipeline %s...', pipeline.id)

            response = self.api_client.import_pipeline(pipeline_id=pipeline.id,
                                                       pipeline_json=pipeline._data)
            try:
                pipeline.id = response['pipelineConfig']['pipelineId']
            except KeyError:
                pipeline.id = response['pipelineConfig']['info']['name']

    def get_pipeline_builder(self):
        """Get a PipelineBuilder instance with which a Pipeline can be created.

        Returns:
            An instance of :py:class:`streamsets.PipelineBuilder`
        """

        # A PipelineBuilder instance takes an empty pipeline and a list of stage definitions as
        # arguments. To get the former, we generate a pipeline in SDC, export it, and then delete
        # it. For the latter, we simply pass along `self.stage_definitions`.
        create_pipeline_command = self.api_client.create_pipeline(pipeline_title='Pipeline Builder',
                                                                  auto_generate_pipeline_id=True)
        try:
            pipeline_id = create_pipeline_command.response.json()['info']['pipelineId']
        except KeyError:
            pipeline_id = create_pipeline_command.response.json()['info']['name']

        pipeline = self.api_client.export_pipeline(pipeline_id)
        self.api_client.delete_pipeline(pipeline_id)

        return sdc_models.PipelineBuilder(pipeline=pipeline,
                                          stage_definitions=self.stage_definitions)

    @property
    def stage_definitions(self):
        """Get an SDC instance's stage definitions.

        Will return a cached instance of the stage definitions if called more than once.
        """
        if self._stage_definitions:
            return self._stage_definitions

        self._stage_definitions = self.api_client.get_definitions()['stages']
        return self._stage_definitions
