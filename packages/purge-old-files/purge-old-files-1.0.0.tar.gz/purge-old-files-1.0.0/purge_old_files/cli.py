from argparse import ArgumentParser
import logging
from os import unlink
import sys

from purge_old_files import filters, age, finder


LOGGER = logging.getLogger(__name__)
DEFAULT_MESSAGE_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)s %(message)s'
DEFAULT_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


def parse_arguments(argv=None):
    """Parse command line arguments.
    """
    parser = ArgumentParser()

    parser.add_argument(
        '--debug', '-D', action='store_true', default=False,
        help='Show debug messages')
    parser.add_argument(
        '--dry-run', '-d', action='store_true', default=False,
        help='Show which files should be deleted')
    parser.add_argument(
        '--include', '-i', metavar='PATTERN', dest='filters', action='append',
        type=filters.glob, help='Include only files matching pattern')
    parser.add_argument(
        '--exclude', '-e', metavar='PATTERN', dest='filters', action='append',
        type=lambda x: filters.negate(filters.glob(x)),
        help='Exclude files matching pattern')
    parser.add_argument(
        'filters', metavar='MIN_AGE', action='append',
        type=lambda x: filters.age(age.parse(x)),
        help='Minimum age of files')
    parser.add_argument(
        'directory', metavar='DIRECTORY', help='Directory to be scanned')

    return parser.parse_args(argv)


def configure_logging(debug=False,
                      message_format=DEFAULT_MESSAGE_FORMAT,
                      date_format=DEFAULT_DATE_FORMAT,
                      stream=sys.stdout):
    """Configure logging.
    """
    level = logging.DEBUG if debug else logging.INFO
    formatter = logging.Formatter(message_format, date_format)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)


def main(argv=None):
    """Command line entry point.
    """
    arguments = parse_arguments(argv)
    configure_logging(arguments.debug)

    files = finder.find(arguments.directory, arguments.filters)

    for file_ in files:
        if arguments.dry_run:
            LOGGER.info('To be deleted: %s', file_)
        else:
            LOGGER.info('Deleting: %s', file_)
            unlink(file_.path)

    if arguments.dry_run:
        LOGGER.info('%s files to be deleted', len(files))
    else:
        LOGGER.info('Deleted %s files', len(files))
