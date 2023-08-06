#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the cli of the s3_analyst package."""

from string import ascii_letters

import pytest

from s3_analyst import cli

import boto3
from moto import mock_s3

from hypothesis import given
from hypothesis.strategies import just, lists, text
from freezegun import freeze_time


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
    from s3_analyst import s3_analyst
    s3_analyst.init_csv_file(str(test))
    return test


@given(lists(text(ascii_letters, min_size=1), min_size=1))
def test_cli_bucket_option(capsys, bucket_list):
    """
    Test if the cli recognizes the bucket option.
    """
    try:
        if isinstance(bucket_list[0], unicode):  # noqa
            new_bucket_list = []
            for item in bucket_list:
                new_bucket_list.append(item.encode('utf-8', 'ignore'))
            bucket_list = new_bucket_list
    except Exception:
        # hypothesis.strategies.text generates str on Python3, unicode on 2.7.
        # docopt fails to read repeating elements if unicode is used
        # https://github.com/docopt/docopt/issues/301
        # https://github.com/docopt/docopt/issues/219
        pass
    from docopt import docopt

    doc = cli.__doc__
    args = docopt(doc, bucket_list)
    out, _ = capsys.readouterr()
    print(out)
    assert args["<buckets>"] == bucket_list


@given(just(['firstbucket', 'secondbucket']))
def test_cli_parser_bucket_list(no_user_dependant, fake_s3, bucket_list):
    """
    Test if cli.parser returns the list of buckets.
    """
    s3_resource = fake_s3().resource

    from docopt import docopt
    doc = cli.__doc__
    args = docopt(doc, bucket_list)
    result = cli.parser(args)

    assert result == {
        '--block_data_crunching': False,
        '--default_timeout': 60,
        '--exclude-mine': False,
        '--filename': None,
        '--filepath': None,
        '--fmtsize': '',
        '--force_update': False,
        '--path': None,
        '--regex': None,
        '<buckets>': bucket_list,
        'bucket_list': list(map(lambda bucket_name:
                                s3_resource.Bucket(name=bucket_name),
                                bucket_list)),
        'filepath': no_user_dependant+'/aws_s3_export.csv'}


@pytest.mark.parametrize("fmt_size", ['B',
                                      'KB', 'MB', 'GB',
                                      'KiB', 'MiB', 'GiB',
                                      'TB', 'PB', 'EB', 'ZB',
                                      'TiB', 'PiB', 'EiB', 'ZiB'])
def test_cli_parser_fmtsize(no_user_dependant, fake_s3, fmt_size):
    """
    Test if the cli.parser prints the message as expected.
    """
    fake_s3 = fake_s3().resource

    from docopt import docopt
    doc = cli.__doc__
    args = docopt(doc, ["firstbucket", '--exclude-mine',
                        '--fmtsize', fmt_size])
    out = cli.parser(args)
    expected_output = {
        '--block_data_crunching': False,
        '--default_timeout': 60,
        '--exclude-mine': True,
        '--filename': None,
        '--filepath': None,
        '--fmtsize': fmt_size,
        '--force_update': False,
        '--path': None,
        '--regex': None,
        '<buckets>': ['firstbucket'],
        'bucket_list': [fake_s3.Bucket(name='firstbucket')],
        'filepath': no_user_dependant+'/aws_s3_export.csv'}
    assert out == expected_output


def test_cli_parser_invalid_option():
    """
    Test if the cli.parser raises a schema error if an option is invalid.
    """
    from docopt import docopt
    from schema import SchemaError
    doc = cli.__doc__
    args = docopt(doc, ["firstbucket", '--fmtsize', 'To'])
    with pytest.raises(SchemaError):
        cli.parser(args)


def test_cli_parser_validation():
    """
    Test if the cli.parser prints a user-friendly message on failure.
    """
    from docopt import docopt
    from schema import SchemaError
    expected_output = ("'validate' raised SchemaError('fmtsize option should "
                       "respect the format : B, KB, KiB, MB, MiB, GB, GiB, "
                       "TB, TiB, PB, PiB, EB, EiB, ZB, ZiB.',)")
    with pytest.raises(SchemaError):
        try:
            doc = cli.__doc__
            args = docopt(doc, ["firstbucket", '--fmtsize', 'Mo'])
            cli.parser(args)
        except SchemaError as err:
            assert err.args[0] == expected_output
            raise


def test_cli_main(no_user_dependant, fake_s3):
    """
    Test if the cli.main exits when no arg.
    Note: sys.argv should not have any extra option after name of the test.
    """
    with pytest.raises((EOFError, SystemExit)):
        # raise EOFError because bucket list is empty.
        # raise Docopt.DocoptExit if sys.argv contains invalid option.
        cli.main()


def test_cli_main_help(capsys):
    """
    Test cli.main with help in sys.argv.
    """
    import sys
    doc = cli.__doc__
    sys.argv.append("-h")
    with pytest.raises(SystemExit):
        cli.main()
    out, _ = capsys.readouterr()
    assert out == doc


def test_cli_main_output(fake_s3, a_file):
    """
    Test how cli.main reacts with a list of args.
    """
    from datetime import datetime
    a_datetime = datetime(2010, 11, 12, 13, 14, 15)

    # Reduce non-determinism properties
    with freeze_time(a_datetime):

        # Configure the fake s3
        empty_s3 = fake_s3(a_file)
        empty_s3.false_bucket('firstbucket')
        empty_s3.fill_bucket('firstbucket', 'falseBucket.test')

        arguments = ["firstbucket", '--fmtsize', 'KB',
                     '--filepath', str(a_file), '--force_update']
        out = cli.main(arguments)

        mtime_fmt = a_datetime.strftime('%Y-%m-%d %H:%M:%S')
        # modif_time_fmt = datetime.utcfromtimestamp(
        #     a_file.mtime()).strftime('%Y-%m-%d %H:%M:%S')

        expected_output = [{
            'object': 1, 'bucket name': 'firstbucket', 'filter': None,
            'location': 'us-east-1', 'creation date': '2006-02-03 16:45:09',
            'size': '0.1KB', 'last modified date': mtime_fmt}]
        assert out == expected_output
