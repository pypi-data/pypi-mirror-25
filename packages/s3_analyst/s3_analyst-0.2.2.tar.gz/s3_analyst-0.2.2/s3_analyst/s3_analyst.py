#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A module which contains functions to crunch aws s3 metadata
and query over them.
"""

import csv
import datetime
import logging

import os.path
from os import error

import boto3
from botocore.exceptions import ClientError

import pandas as pd

try:
    from s3_analyst import s3_analyst_logging
except ImportError:  # pragma: no cover
    import s3_analyst_logging

# configure the logger
s3_analyst_logging.setup_logging()
LOGGER = logging.getLogger(__name__)

# declare aws variables
S3 = boto3.resource("s3")
S3_CLIENT = boto3.client("s3")


def default_csv_path(directory=None):
    """
    Return the given directory or set up a default one.
        :directory=expanduser("~"): String - given absolute directory.
    """
    if directory is None:
        directory = os.path.expanduser("~")
    return directory


def default_csv_filename(filename='aws_s3_export.csv'):
    """
    Return the given filename or set up a default one.
        :param filename='aws_s3_export.csv': String - given filename
    """
    return filename


def default_csv_filepath(
        path=None,
        filename=None):
    """
    Return the filepath given the path and the filename.
        :param path=default_csv_path(): String - given absolute directory
        :param filename=default_csv_filename(): String - given filename

    """
    if path is None:
        path = default_csv_path()
    if filename is None:
        filename = default_csv_filename()
    filepath = os.path.join(path, filename)
    return filepath


def init_csv_file(filepath=default_csv_filepath()):
    """
    Write headers of a csv file.\
    Return the filepath.
        :filepath=default_csv_filepath(): the absolute csv filepath
    """
    headers = [
        "bucket name",
        "location",
        "creation date",
        "object",
        "last modified date",
        "owner",
        "size",
        "storage class"]  # TODO(tofull) Pass this list as args

    with open(filepath, 'w') as file:
        wrt = csv.writer(file, quoting=csv.QUOTE_ALL)
        wrt.writerow(headers)

    return filepath


def crunch_data(filepath, bucket_list=None):
    """
    Crunch data and fill the csv file given by the filepath with informations
    from a list of buckets.
        :param filepath: Absolute path for csv file.
        :param bucket_list=None: The list of buckets.
    """

    bucket_info = [0 for _ in range(8)]

    with open(filepath, 'a') as export:
        wrt = csv.writer(export, quoting=csv.QUOTE_ALL)

        for bucket in bucket_list:
            try:
                location = S3_CLIENT.get_bucket_location(
                    Bucket=bucket.name
                )['LocationConstraint']
            except ClientError as cli_err:  # pragma: no cover
                LOGGER.error("Received error: %s", cli_err, exc_info=True)
                location = 'Unabled to find'

            try:
                bucket_creation_date = bucket.creation_date.strftime(
                    "%Y-%m-%d %H:%M:%S")
            except AttributeError as att_err:  # pragma: no cover
                LOGGER.error("Received error: %s", att_err, exc_info=True)
                bucket_creation_date = 'Unable to find'

            prefix = bucket.name + '/'
            for key in bucket.objects.all():
                # bucket.objects.all() returns a list of s3.objectSummary items
                time_format = key.last_modified
                formated_time = time_format.strftime("%Y-%m-%d %H:%M:%S")

                bucket_info[0] = bucket.name
                bucket_info[1] = location
                bucket_info[2] = bucket_creation_date
                bucket_info[3] = prefix + key.key
                bucket_info[4] = formated_time
                bucket_info[5] = key.owner['ID']
                bucket_info[6] = key.size
                bucket_info[7] = key.storage_class
                wrt.writerow(bucket_info)


def is_file_expired(filepath, threshold=60):
    """
    Return True if the file was created before a certain amount of time.
    Else otherwise.
        :param filepath: Absolute path to the file.
        :param threshold=60: Number of seconds.
    """
    try:
        date = os.path.getctime(filepath)
    except error:
        LOGGER.debug("Unable to get the creation date of %s.", filepath)
        return True
    now = datetime.datetime.now().timestamp()
    # nom = time.time()  # for python2 but bug with freeze_time in tests.
    # datetime.timestamp does not exist on python2...
    # >> This package does not support python2 anymore.
    ellapsed = now - date
    return ellapsed > threshold


def collect_informations(filepath, regex_filtering="^[a-z]*"):
    """
    Extract informations from csv file where bucket data are stored.
        :param filepath: Absolute filepath of the csv file
        :param regex_filtering: Regex to filter the result
    """

    try:
        data = pd.read_csv(filepath)
    except pd.errors.ParserError as pderror:
        raise EOFError('%s\n\nYour csv file may be empty. '
                       'Please try with the --force_update option or check '
                       'your bucket list.' % pderror)
    try:
        out = data.loc[data.loc[:, 'object'].str.contains(regex_filtering)]
    except TypeError:
        out = data

    out = out.groupby(['bucket name'], as_index=False).agg({
        'creation date': 'unique',
        'location': 'unique',
        'object': 'count',
        'size': 'sum',
        'last modified date': 'max'})

    buckets_info = []
    for bucket_index in range(len(out['bucket name'])):
        info = {
            'bucket name': out['bucket name'][bucket_index],
            'creation date': out['creation date'][bucket_index][0],
            'location': out['location'][bucket_index][0],
            'object': out['object'][bucket_index],
            'size': out['size'][bucket_index],
            'last modified date': out['last modified date'][bucket_index]
        }
        buckets_info.append(info.copy())

    return buckets_info


def sizeof_fmt(bytes_size, forced_unit='B'):
    """
    Convert the size into a more human readable format.
    The final unit could be forced by the second param.
        :param bytes_size: Size to convert (in bytes)
        :param forced_unit='B': Output unit. Could be choosen between :
            B, KB, MB, GB, TB, PB, EB, ZB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB

    Note : Inspired from
    https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size # noqa #pylint: disable
    """

    forced_unit = forced_unit.lower()

    if 'i' in forced_unit:
        divisor = 1024.0
        units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']
    else:
        divisor = 1000.0
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']

    lower_units = map(str.lower, units)

    if forced_unit in lower_units or forced_unit == '':
        for unit in units:
            if ((abs(bytes_size) < divisor and forced_unit == '')
                    or forced_unit == unit.lower()):
                if isinstance(bytes_size, int):
                    if bytes_size > 9007199254740992:
                        print(bytes_size)
                        raise ArithmeticError('The bytes_size variable '
                                              '(value : %s) is not convenient '
                                              'with IEEE754 standard. It is '
                                              'not a representable integer, '
                                              'that means it is upper than '
                                              '2^54+1'
                                              % (bytes_size))
                return "%3.1f%s" % (bytes_size, unit)
            bytes_size /= divisor
    return "%.1f%s" % (bytes_size, 'B')


def format_output(output, **kwargs):
    """
    Format the output to have a better display of the collected informations.
        :param output: Dictionnary containing all the collected informations.
        :param **kwargs: any option like size, filter, and so on...
    """
    size = kwargs.get('size', 'B')
    size = size.title()
    output['size'] = str(sizeof_fmt(output['size'], forced_unit=size))

    filter_expression = kwargs.get('filter', None)
    output['filter'] = filter_expression

    return output


def str_to_bucket_list(string_list=None, own_buckets=True):
    """
    Convert a string list into a bucket list.
        :param string_list=[]: A string list
        :param own_buckets=True: If True, include all buckets from S3 resource.

    > str_to_bucket_list([dc-lidar-2015], own_buckets=False)
    >>> [s3.Bucket(name='dc-lidar-2015')]
    > str_to_bucket_list([dc-lidar-2015], own_buckets=True)
    >>> [s3.Bucket(name='testcoveotofull'), s3.Bucket(name='dc-lidar-2015')]
    """

    if string_list is None:
        string_list = []
    bucket_list = []
    if own_buckets:
        bucket_list = list(S3.buckets.all())
    for item in string_list:
        bucket_to_append = S3.Bucket(item)
        if bucket_to_append not in bucket_list:
            bucket_list.append(S3.Bucket(item))

    return bucket_list


def main(**kwargs):
    '''
    Main function
    '''
    force_update = kwargs.get('force_update', False)
    bucket_list = kwargs.get('bucket_list', None)
    default_timeout = kwargs.get('default_timeout', 60)
    filepath = kwargs.get('filepath', default_csv_filepath())
    block_data_crunching = kwargs.get('block_data_crunching', False)
    regex_filtering = kwargs.get('regex_filtering', '^[a-z]*')
    fmt_size = kwargs.get('fmt_size', "B")

    if ((is_file_expired(filepath, default_timeout) or force_update)
            and not block_data_crunching):
        LOGGER.warning("The csv file will be replaced \
        (too old or update forced by user)")
        LOGGER.debug("Csv file location : %s", filepath)
        init_csv_file(filepath)
        LOGGER.info("crunching data from cloud provider")
        crunch_data(filepath, bucket_list)
        LOGGER.info("crunching data ... done")

    infos = collect_informations(filepath, regex_filtering)
    formated_output_list = []
    for info in infos:
        formated_output = format_output(info.copy(),
                                        size=fmt_size,
                                        filter=regex_filtering)
        print(formated_output)
        formated_output_list.append(formated_output.copy())
    return formated_output_list


if __name__ == '__main__':  # pragma: no cover
    import sys
    main(**dict(arg.split('=') for arg in sys.argv[1:]))
