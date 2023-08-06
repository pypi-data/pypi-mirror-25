#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `s3_analyst` package."""

import pytest

from hypothesis import given
from hypothesis.strategies import just, integers, floats, text
from freezegun import freeze_time

import boto3
from moto import mock_s3

from s3_analyst import s3_analyst


@pytest.yield_fixture(scope="function")
def fake_s3():
    """
    A pytest fixture to simulate aws s3 storage behaviours.
    """
    mock_s3().start()

    class FakeS3(object):
        """
        A fake s3 storage which contains calls to client and resource.
        """
        def __init__(self, file=None):
            self.client = boto3.client("s3")
            self.resource = boto3.resource("s3")
            self.file = str(file)

        def false_bucket(self, name):
            """
            Create a false bucket.
                :name: Given name to the bucket.
            """
            self.resource.create_bucket(Bucket=name)

        def fill_bucket(self, bucket_name, bucket_key):
            """
            Add the content of self.file to a new key into the bucket.
            """
            bucket = self.resource.Bucket(bucket_name)
            with open(self.file, 'rb') as body:
                bucket.put_object(Key=bucket_key, Body=body)

    yield FakeS3

    mock_s3().stop()


@pytest.fixture()
def no_user_dependant(monkeypatch, tmpdir):
    """
    Replace os.path.expanduser by a directory created for the test.
    """
    import os.path

    def mockreturn(_):
        """
        Mock expanduser.
        """
        return str(tmpdir)
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)
    return str(tmpdir)


@pytest.fixture(scope="function")
def a_file(tmpdir):
    """
    Generate a file in a structured format for the test.
    """
    test = tmpdir.join('file.csv')
    s3_analyst.init_csv_file(str(test))
    return test


@pytest.fixture()
def no_time_dependant(monkeypatch):
    """
    Replace os.path.getctime by a fixed timestamp for the test.
    """
    import os.path
    from datetime import datetime

    a_datetime = datetime(2010, 11, 12, 13, 14, 15)

    def mockreturn(_):
        """
        Mock getctime.
        """
        return a_datetime.timestamp()

    monkeypatch.setattr(os.path, 'getctime', mockreturn)
    return a_datetime


def test_collect_informations():
    """
    Test s3_analyst.collect_informations with a csv sample file.
    """
    import os
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filepath = os.path.join(current_file, 'data/aws_s3_export_2.csv')

    buckets_info = s3_analyst.collect_informations(csv_filepath)

    assert buckets_info == [
        {
            'creation date': '2017-09-16 08:59:36',
            'object': 1,
            'size': 81897,
            'location': 'eu-central-1',
            'last modified date': '2017-09-16 09:12:11',
            'bucket name': 'testcoveoprotony'
        }, {
            'creation date': '2017-09-16 08:58:36',
            'object': 3,
            'size': 90671,
            'location': 'eu-central-1',
            'last modified date': '2017-09-16 09:02:11',
            'bucket name': 'testcoveotofull'}]


@pytest.mark.parametrize("regex_param", [
    "^testcoveop[a-z]*",
    "^[a-z]*protony[a-z]*",
    "proto",
    "[a-z]*y"
    ])
def test_collect_info_regex_filter(regex_param):
    """
    Test collect_informations with a csv sample file and filter option. \
    Filter are designed to return information about \
    the testcoveoprotony bucket name.
    """
    import os
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filepath = os.path.join(current_file, 'data/aws_s3_export_2.csv')

    regex_filter = regex_param
    buckets_info = s3_analyst.collect_informations(csv_filepath, regex_filter)
    assert buckets_info == [
        {
            'creation date': '2017-09-16 08:59:36',
            'object': 1,
            'size': 81897,
            'location': 'eu-central-1',
            'last modified date': '2017-09-16 09:12:11',
            'bucket name': 'testcoveoprotony'
        }]


def test_init_csv_file(tmpdir):
    """
    Test if the new csv output file has headers as expected.
    """
    csv_file = tmpdir.join('output.csv')
    s3_analyst.init_csv_file(str(csv_file))
    with open(str(csv_file), 'rU') as file:
        assert file.read() == ('"bucket name","location","creation date",'
                               '"object","last modified date","owner","size",'
                               '"storage class"\n')


@given(floats())
def test_sizeof_fmt_floats(bytes_size):
    """
    Test the sizeof_fmt function with floats.
    """
    output = s3_analyst.sizeof_fmt(bytes_size, forced_unit='B')
    assert output == '{:3.1f}'.format(bytes_size)+'B'


@given(integers(max_value=9007199254740992))
def test_sizeof_fmt_integers(bytes_size):
    """
    Test the sizeof_fmt function with integers.

    If bytes_size is an integer, it should be a "valid" integers, \
    ie. it should respect the IEEE 754 standard. That means some problems \
    could occur because, any number requiring more than 52 significant \
    bits is rounded to 52 significant bits. And 2^53 = 9007199254740992.
    `See more details. <https://stackoverflow.com/q/3793838>`_
    """
    output = s3_analyst.sizeof_fmt(bytes_size, forced_unit='B')
    assert output == str(bytes_size)+'.0B'


@given(integers(min_value=9007199254740993))
def test_sizeof_fmt_invalid_int(bytes_size):
    """
    Test the sizeof_fmt function with invalid integers.

    If bytes_size is an integer, it should be a "valid" integers, \
    ie. it should respect the IEEE 754 standard. That means some problems \
    could occur because, any number requiring more than 52 significant \
    bits is rounded to 52 significant bits. And 2^53 = 9007199254740992.
    `See more details. <https://stackoverflow.com/q/3793838>`_
    """
    with pytest.raises(ArithmeticError):
        s3_analyst.sizeof_fmt(bytes_size, forced_unit='B')


@pytest.mark.parametrize("bytes_size,unit,expected", [
    (0, 'B', "0.0B"),
    (0, 'MB', "0.0MB"),
    (1000, 'KB', "1.0KB"),
    (1024, 'KiB', "1.0KiB"),
    (9000, 'KB', "9.0KB"),
    (9234, 'KB', "9.2KB"),
    (9734, 'KB', "9.7KB"),
    (10000, 'KB', "10.0KB"),
    (100000, 'KB', "100.0KB"),
    (1000000, 'KB', "1000.0KB"),
    (1000000, 'KiB', "976.6KiB"),
    (1000000, 'MB', "1.0MB"),
    (10000000, 'KB', "10000.0KB"),
    (10000000, 'MB', "10.0MB"),
    (1000000000, 'GB', "1.0GB"),
    (1000000000000, 'TB', "1.0TB"),
    (1000000000000000, 'PB', "1.0PB"),
    (1000000000000000000, 'EB', "1.0EB"),
    (100000000000000000000, 'ZB', "0.1ZB"),
    (1000000000000000000000, 'ZB', "1.0ZB"),
    (1000000000000000000000, 'KB', "1000000000000000000.0KB"),
])
def test_sizeof_fmt_param_unit(bytes_size, unit, expected):
    """
    Test sizeof_fmt given a forced_unit.
    """
    output = s3_analyst.sizeof_fmt(bytes_size, forced_unit=unit)
    assert output == expected


@pytest.mark.parametrize("bytes_size,expected_output", [
    (0, "0.0B"),
    (1000, "1.0KB"),
    (1024, "1.0KB"),
    (9000, "9.0KB"),
    (9234, "9.2KB"),
    (9734, "9.7KB"),
    (10000, "10.0KB"),
    (100000, "100.0KB"),
    (409600, "409.6KB"),
    (1000000, "1.0MB"),
    (1000000, "1.0MB"),
    (10000000, "10.0MB"),
    (409600425, "409.6MB"),
    (4096004250, "4.1GB"),
    (1000000000, "1.0GB"),
    (1000000000000, "1.0TB"),
    (1000000000000000, "1.0PB"),
    (1000000000000000000, "1.0EB"),
    (100000000000000000000, "100.0EB"),
    (1000000000000000000000, "1.0ZB"),
])
def test_sizeof_fmt_parametrized(bytes_size, expected_output):
    """
    Test sizeof_fmt given an empty forced_unit (auto-choosen unit mode).
    """
    output = s3_analyst.sizeof_fmt(bytes_size, forced_unit='')
    assert output == expected_output


@given(integers(
    max_value=9007199254740992),
       text().filter(lambda txt:
                     txt not in [''] +
                     ['B', 'KB', 'MB', 'GB',
                      'TB', 'PB', 'EB', 'ZB'] +
                     ['B', 'KiB', 'MiB', 'GiB',
                      'TiB', 'PiB', 'EiB', 'ZiB']))
def test_sizeof_fmt_invalid_unit(bytes_size, forced_unit):
    """
    Test sizeof_fmt given an invalid unit. Should return the output without \
    change but in B.
    """
    output = s3_analyst.sizeof_fmt(bytes_size, forced_unit=forced_unit)
    assert output == str(bytes_size)+'.0B'


def test_format_output():
    """
    Test format_output with minimal input.
    """
    arg = {'size': 0}
    out = s3_analyst.format_output(arg)
    assert out == {'size': '0.0B', 'filter': None}


def test_format_output_filter():
    """
    Test format_output with minimal input and filter option.
    """
    arg = {'size': 0}
    regex_filter = '^[a-z]*'
    out = s3_analyst.format_output(arg, filter=regex_filter)
    assert out == {'size': '0.0B', 'filter': regex_filter}


def test_is_file_expired_notexist(tmpdir):
    """
    Test if a file is expired when it does not exist.
    """
    file = tmpdir.join('notexist.csv')
    out = s3_analyst.is_file_expired(str(file), threshold=60)
    assert out


def test_is_expired_just_created(tmpdir):
    """
    Test if a file is expired when threshold = 0.
    """
    file = tmpdir.join('output.csv')
    s3_analyst.init_csv_file(str(file))
    out = s3_analyst.is_file_expired(str(file), threshold=0)
    assert out


@pytest.mark.parametrize("seconds,threshold,expected", [
    (10, 60, False),  # "50 seconds until expired"
    (61, 60, True),  # "expired from 1 second"
    (59, 60, False),  # "1 second until expired"
    (1, 0, True),  # "expired from 1 second"
    (10, 0, True),  # "expired from 10 seconds"
    (0, 0, False),  # "get the limit"
    (60, 60, False),  # "get the limit"
    (0, 1, False),  # "1 second until expired"
])
def test_is_file_expired(tmpdir, no_time_dependant, seconds,
                         threshold, expected):
    """
    Test if a file is expired with travelling in time.
    """
    from datetime import timedelta

    # Reduce non-determinism properties
    a_datetime = no_time_dependant
    a_timedelta = timedelta(seconds=seconds)
    fake_datetime = a_datetime + a_timedelta

    # Create file at date a_datetime
    with freeze_time(a_datetime):
        file = tmpdir.join('output.csv')
        s3_analyst.init_csv_file(str(file))

    # Check if it is expired at a_datetime + a_timedelta
    with freeze_time(fake_datetime):
        out = s3_analyst.is_file_expired(str(file), threshold=threshold)
        assert out == expected


def test_str_to_bucket_list_empty():
    """
    Test the conversion from a empty str list to bucket list.
    """
    out = s3_analyst.str_to_bucket_list(string_list=[], own_buckets=False)
    assert out == []


def test_str_to_bucket_list_none():
    """
    Test the conversion from a None str list to bucket list.
    """
    out = s3_analyst.str_to_bucket_list(string_list=None, own_buckets=False)
    assert out == []


@given(just(['firstbucket', 'secondbucket']))
def test_str_to_bucket_list(fake_s3, bucket_list):
    """
    Test the conversion from a str list to bucket list.
    """
    s3_resource = fake_s3().resource
    out = s3_analyst.str_to_bucket_list(
        string_list=bucket_list, own_buckets=False)
    assert out == list(map(lambda bucket_name:
                           s3_resource.Bucket(name=bucket_name),
                           bucket_list))


def test_crunch_data(fake_s3, a_file):
    """
    Test if crunch_data write all the information from the fake s3 storage.
    """
    from datetime import datetime
    a_datetime = datetime(2010, 11, 12, 13, 14, 15)

    # Reduce non-determinism properties
    with freeze_time(a_datetime):
        # Configure the fake s3
        empty_s3 = fake_s3(a_file)
        empty_s3.false_bucket('firstbucket')
        empty_s3.fill_bucket('firstbucket', 'falseBucket.test')
        a_bucket = empty_s3.resource.Bucket('firstbucket')

        # Crunch data and compare with the expected output
        s3_analyst.crunch_data(str(a_file), bucket_list=[a_bucket])

        mtime_fmt = a_datetime.strftime('%Y-%m-%d %H:%M:%S')
        expected_output = (
            '"bucket name","location","creation date","object",'
            '"last modified date","owner","size","storage class"\n'
            '"firstbucket","us-east-1","2006-02-03 16:45:09",'
            '"firstbucket/falseBucket.test","%s",'
            '"75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a'
            '","103","STANDARD"\n') % mtime_fmt
        with open(str(a_file), 'rU') as file:
            assert file.read() == expected_output


def test_main(fake_s3, a_file):
    """
    Test if the main function write all the information from the fake \
    s3 storage and return the information.
    """
    from datetime import datetime
    a_datetime = datetime(2010, 11, 12, 13, 14, 15)

    # Reduce non-determinism properties
    with freeze_time(a_datetime):
        # Configure the fake s3
        empty_s3 = fake_s3(a_file)
        empty_s3.false_bucket('firstbucket')
        empty_s3.fill_bucket('firstbucket', 'falseBucket.test')
        a_bucket = empty_s3.resource.Bucket('firstbucket')

        # Crunch data and compare with the expected output
        out = s3_analyst.main(**dict(
            bucket_list=[a_bucket],
            force_update=True,
            filepath=str(a_file)))

        mtime_fmt = a_datetime.strftime('%Y-%m-%d %H:%M:%S')
        expected_output = (
            '"bucket name","location","creation date","object",'
            '"last modified date","owner","size","storage class"\n'
            '"firstbucket","us-east-1","2006-02-03 16:45:09",'
            '"firstbucket/falseBucket.test","%s",'
            '"75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a'
            '","103","STANDARD"\n'
            ) % mtime_fmt

        with open(str(a_file), 'rU') as file:
            assert file.read() == expected_output

        expected_output = [{
            'location': 'us-east-1',
            'filter': '^[a-z]*',
            'last modified date': mtime_fmt,
            'size': '103.0B',
            'creation date': '2006-02-03 16:45:09',
            'bucket name': 'firstbucket',
            'object': 1}]
        assert out == expected_output
