#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the s3_analyst_logging part of the s3_analyst package."""

from s3_analyst import s3_analyst_logging


def test_setup_logging_default():
    """
    Test s3_analyst_logging.setup_logging with the default argument.
    Should use a predefined yaml config file.
    """
    output = s3_analyst_logging.setup_logging()
    assert output == 'logging is using a yaml config file'


def test_setup_logging_basic_config():
    """
    Test s3_analyst_logging.setup_logging with a bad config path.
    Should use the basic config.
    """
    output = s3_analyst_logging.setup_logging(None)
    assert output == 'logging is using basic config'
