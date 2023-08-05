# Copyright 2017 StreamSets Inc.

import logging
import os

from .config import USER_CONFIG_PATH
from .sdc import DataCollector
from .sdc_models import (Configuration, DataRule, DataDriftRule,  # NOQA
                         Pipeline, PipelineBuilder, Stage)

__all__ = ['DataCollector']

__version__ = '1.1.0'

logger = logging.getLogger(__name__)

activation_path = os.path.join(USER_CONFIG_PATH, 'activation')

if not os.path.exists(activation_path):
    logger.info('Creating user configuration directory at %s ...', USER_CONFIG_PATH)
    os.makedirs(activation_path)
