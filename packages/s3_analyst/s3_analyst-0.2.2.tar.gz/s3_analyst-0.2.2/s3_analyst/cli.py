#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""S3 analyst for Coveo Devops challenge. This tool will crunch metadata from \
S3 storage, store them into a local csv file and query over it. You can share \
your csv file with ease, automate its build, or re-use it again and again.

Usage:
  cli.py [<buckets>...] [--exclude-mine] [--fmtsize FMTSIZE] \
[--regex=<filter>] [(--block_data_crunching | \
[--force_update --default_timeout=<x>])] [[--path=<abs_path>] \
[--filename=<filename>] | --filepath=<full_filename>]
  cli.py [<buckets>...]
  cli.py [<buckets>...] [--exclude-mine]
  cli.py [<buckets>...] [--exclude-mine] [--regex=<filter>]
  cli.py [<buckets>...] [--exclude-mine] [--fmtsize FMTSIZE]
  cli.py [<buckets>...] [--exclude-mine] [(--block_data_crunching | \
[--force_update --default_timeout=<x>])]
  cli.py [<buckets>...] [--regex=<filter>] [[--path=<abs_path>] \
[--filename=<filename>] | --filepath=<full_filename>]

Examples:
  >>> # Crunch data from aws public dataset [without yours for genericity]
  >>> cli.py dc-lidar-2015 --exclude-mine --force_update
  >>> # Crunch data quicker from aws public dataset (using cache)
  >>> cli.py dc-lidar-2015 -e
  >>> # Be the force with you and crunch data from aws public dataset \
(ignore cache)
  >>> cli.py dc-lidar-2015 -e --force_update
  >>> # Filter metadata with regex and avoid to crunch metadata again \
(force using cache)
  >>> cli.py -e --block_data_crunching --regex='2011'
  >>> # Shortest filter metadata with regex (force using cache with -b option)
  >>> cli.py -eb --regex='2011'
  >>> # An example of a little more complex regex
  >>> cli.py -eb --regex='^dc-lidar-2015/Classified_LAS/11[a-z]*'
  >>> # You can change the size unit
  >>> cli.py -eb --fmtsize TB
  >>> # Wow, this tool begins to be impressive, isn't it?
  >>> # Let's go deeper in foolish!
  >>> # You can also get informations of multiple buckets. \
[Here is another public dataset hosted on aws] \
[NB: about 1 minute is required depending how your Internet is.]
  >>> cli.py -e dc-lidar-2015 fmi-opendata-rcrhirlam-surface-grib \
--force_update
  >>> # That's a lot of data !
  >>> # Now, it's time to work together.
  >>> # Let's crunch the data again in another csv file.
  >>> cli.py dc-lidar-2015 --exclude-mine --path="/home/${USER}" \
--filename='another_cache.csv'
  >>> # Or more consise way
  >>> cli.py dc-lidar-2015 --exclude-mine \
--filepath="/home/${USER}/another_cache.csv"
  >>> # Let's play or check the documentation on the Internet for more options
  >>> cli.py --help

Options:
  <buckets>                     The name of the buckets to analyze.

  -h, --help                    Show this screen.
  -v, --version                 Show version.
  --fmtsize unit                Format the display of the size in the results.
                                    Leave blank for auto-choosen unit.
                                    Unit should be one of :
                                    '', 'B', 'KB', 'KiB', 'MB', 'MiB', 'GB',
                                    'GiB', 'TB', 'TiB', 'PB', 'PiB', 'EB',
                                    'EiB', 'ZB', 'ZiB'
                                    [default: ].
  -e, --exclude-mine            Do not consider your own buckets.
                                    [default: False].
  --regex=<filter>              Regex to filter the bucket output.
  -b, --block_data_crunching    Avoid to collect data from the Internet.
  -u, --force_update            Force to collect data from the Internet.
  --default_timeout=<x>         Set an amount of seconds to consider the
                                    collected data file as expired.
                                    [default: 60]
  --path=<abs_path>             Full path of directory to store data.
  --filename=<filename>         Name of the file to store data.
  --filepath=<full_filename>    Name of the file to store data. Path included.
"""

import logging
from docopt import docopt

try:
    from s3_analyst.__init__ import __version__
    from s3_analyst import s3_analyst, s3_analyst_logging
except ImportError:  # pragma: no cover
    import s3_analyst
    import s3_analyst_logging
    from __init__ import __version__

from schema import Schema, SchemaError, Or

# configure the logger
s3_analyst_logging.setup_logging()
LOGGER = logging.getLogger(__name__)


def validate(opts):
    """
    Check the opts inputs to respect a specific format.
    """
    schema = Schema({
        '<buckets>':  Or(None, str, [str]),
        '--fmtsize':   Or(None, '', 'B', 'KB', 'KiB', 'MB', 'MiB', 'GB',
                          'GiB', 'TB', 'TiB', 'PB', 'PiB', 'EB', 'EiB',
                          'ZB', 'ZiB',
                          error='fmtsize option should respect the format : '
                                'B, KB, KiB, MB, MiB, GB, GiB, TB, TiB, PB, '
                                'PiB, EB, EiB, ZB, ZiB.'),
        '--exclude-mine': bool,
        '--block_data_crunching': bool,
        '--force_update': bool,
        '--regex': Or(None, str),
        '--default_timeout': int,
        '--path': Or(None, str),
        '--filename': Or(None, str),
        '--filepath': Or(None, str),
    })
    try:
        args = schema.validate(opts)
        return args
    except SchemaError:
        raise


def parser(args):
    """
    Validate args and call some conversion functions.
    """
    # type conversion for validation
    args['--default_timeout'] = int(args['--default_timeout'])

    try:
        validate(args)
    except Exception as error:
        raise SchemaError('%r raised %r' % (validate.__name__, error))

    # type conversion for module
    bucket_list = s3_analyst.str_to_bucket_list(
        args['<buckets>'],
        own_buckets=not args['--exclude-mine'])

    path = args['--path']
    filename = args['--filename']
    filepath = args['--filepath']
    if filepath is None:
        filepath = s3_analyst.default_csv_filepath(path, filename)

    args['bucket_list'] = bucket_list
    args['filepath'] = filepath

    return args


def main(argv=None):
    """
    Decode inputs, call parser and call s3_analyst.main.
    """
    arguments = docopt(__doc__, argv, version=__version__)
    args = parser(arguments)

    kwargs = {}
    kwargs['bucket_list'] = args['bucket_list']
    kwargs['block_data_crunching'] = args['--block_data_crunching']
    kwargs['force_update'] = args['--force_update']
    kwargs['regex_filtering'] = args['--regex']
    kwargs['fmt_size'] = args['--fmtsize']
    kwargs['default_timeout'] = args['--default_timeout']
    kwargs['filepath'] = args['filepath']

    LOGGER.info("cli.main kwargs: %s", kwargs)

    out = s3_analyst.main(**kwargs)

    return out


if __name__ == '__main__':  # pragma: no cover
    main()
