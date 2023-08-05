"""mwdumps

Usage:
    mwdumps --wiki=<wiki_name> [--date=<date>] [--threads=<threads>]
        [--config=<config_file>] [--verbose] <output_path>
    mwdumps (-h | --help)
Options:
    --config=<config_file>       Configuration file containing a set of regexes,
                                    one per line, that matches dump files to be
                                    downloaded.
    --wiki=<wiki_name>           Abbreviation for wiki of interest.
    --date=<date>                Get dump on <date>. Defaults to most recent.
    --threads=<threads>          Number of parallel downloads [default: 3].
    -v, --verbose                Generate verbose output.
"""
from docopt import docopt
from dateutil import parser
import os.path
import os
import logging
from mwdumps.dump import Dump


def _parse_config_file(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f]


def _get_full_output_dir_path(base_output_dir, wiki, date):
    date_str = date.strftime('%Y%m%d')
    return os.path.join(base_output_dir, wiki, date_str)


def _make_output_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def main():
    args = docopt(__doc__)
    if args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    wiki = args['--wiki']
    date = None
    if args['--date'] is not None:
        date = parser.parse(args['--date'])

    regexes = ['.*']
    if args['--config'] is not None:
        regexes = _parse_config_file(args['--config'])

    wikidump = Dump(wiki=wiki, date=date)
    full_output_dir = _get_full_output_dir_path(
        args['<output_path>'], wikidump.wiki, wikidump.date
    )
    _make_output_dir(full_output_dir)

    wikidump.download(
        full_output_dir, matching=regexes, threads=int(args['--threads'])
    )


if __name__ == '__main__':
    main()
