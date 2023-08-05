from __future__ import print_function

import logging
from argparse import ArgumentParser

import backoff
import requests
import sys

url = 'https://coveralls.io/builds/{}.json'


def setup_logging():
    logger = logging.getLogger('backoff')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)


def message(args, covered, template):
    print(template.format(
        args.commit, covered, args.fail_under
    ))


def get_coverage(commit):
    response = requests.get(url.format(commit))
    data = response.json()
    return data['covered_percent']


def decorate(func, args):
    interval = 10
    return backoff.on_predicate(
        backoff.constant,
        interval=interval, max_tries=args.max_wait*60/interval,
        jitter=lambda value: value,
    )(func)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('commit', help='the commit hash to check')
    parser.add_argument('--fail-under', type=float, default=100,
                        help='Exit with a status of 2 if the total coverage is '
                             'less than MIN.')
    parser.add_argument('--max-wait', type=int, default=5,
                        help='Maximum time, in minutes, to wait for Coveralls '
                             'data. Defaults to 5.')
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()
    get_coverage_ = decorate(get_coverage, args)
    covered = get_coverage_(args.commit)
    if covered is None:
        print('No coverage information available for {}'.format(args.commit))
        sys.exit(1)
    elif covered < args.fail_under:
        message(args, covered, 'Failed coverage check for {} as {} < {}')
        sys.exit(2)
    else:
        message(args, covered, 'Coverage OK for {} as {} >= {}')

