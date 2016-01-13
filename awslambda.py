"""
"""
import boto3
from base64 import b64decode
from urlparse import parse_qs
import logging

from calc import find_and_calc


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(params, context):
    results = find_and_calc(params['text'])
    logging.info(
        'Found %d formulas in text "%s" --> %s',
        len(results or []), params['text'], results)

    if results:
        return {
            'text': '\n'.join(
                '`%s = %s`' % (formula, result)
                for formula, result in results
            )
        }

    return None
