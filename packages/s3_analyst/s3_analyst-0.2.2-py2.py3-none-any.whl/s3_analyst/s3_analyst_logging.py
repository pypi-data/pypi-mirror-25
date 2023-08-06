#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Define a function to configure the logging module.
"""

import os
import logging.config

import yaml


def setup_logging(
        default_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'logging.yml'),
        default_level=logging.INFO
):
    """
    Setup logging configuration.
    """
    path = default_path
    try:
        if os.path.exists(path):
            with open(path, 'rt') as file:
                config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)
            return "logging is using a yaml config file"
    except TypeError:
        logging.basicConfig(level=default_level)
        return "logging is using basic config"
