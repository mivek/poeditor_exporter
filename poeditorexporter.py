"""
A Python script
"""

import argparse
import logging
import requests
import sys
from typing import List, Dict

API_URL = 'https://api.poeditor.com/v2/projects/export'

TYPE_CHOICE = ['po', 'pot', 'mo', 'xls', 'xlsx', 'csv', 'ini', 'resw', 'resx',
               'android_strings', 'apple_strings', 'xliff', 'properties',
               'key_value_json', 'json', 'yml', 'xlf', 'xmb', 'xtb', 'arb',
               'rise_360_xliff']

FILTER_CHOICE = ['translated', 'untranslated', 'fuzzy', 'not_fuzzy',
                 'automatic', 'not_automatic', 'proofread', 'not_proofread']


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('poeditorexporter')


def parse_args(argv: List[str]) -> argparse.Namespace:
    """
    Create the argParse parser and specifies the arguments
    :param argv: The list of program arguments
    :return: A namespace with the program's arguments
    """
    parser = argparse.ArgumentParser(prog='poeditorexporter')
    parser.add_argument('api_token', help='Your poeditor api token')
    parser.add_argument('id', help='The id of the project')
    parser.add_argument('languages',
                        help='List of languages comma separated')

    parser.add_argument('dest',
                        help='Destination directory to download files.'
                             'Must end with \'/\'')

    parser.add_argument('filename',
                        help='The name to give to the file once downloaded.'
                             'Will be suffixed by the language')

    parser.add_argument('type',
                        help='The file format',
                        choices=TYPE_CHOICE)

    parser.add_argument('-f', '--filters',
                        help='Filters results, comma separated',
                        choices=FILTER_CHOICE)

    parser.add_argument('-o', '--order',
                        help='Order of the export',
                        default='terms')

    parser.add_argument('-t', '--tags',
                        help='Filter results by tags')
    return parser.parse_args(argv[1:])


def build_payload(args_namespace: argparse.Namespace) -> Dict:
    """
    Builds the payload to send in the request.
    The payload is build from the namespace and
    adds all parameters except the languages
    :param args_namespace:
    :return:
    """
    args_dict = vars(args_namespace)
    args_dict['languages'] = args_dict['languages'].split(',')
    if 'filters' in args_dict and args_dict['filters']:
        args_dict['filters'] = args_dict['filters'].split(',')
    if 'tags' in args_dict and args_dict['tags']:
        args_dict['tags'] = args_dict['tags'].split(',')
    return {key: args_dict[key] for key
            in args_dict.keys() if key != 'languages'}


def process_request(args_dict: dict, lang):
    args_dict['language'] = lang
    logger.info('Retrieving translations for language: %s', lang)
    try:
        r = requests.post(API_URL, data=args_dict)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    data = r.json()
    if r.ok and 'result' in data and data['result']:
        url = data['result']['url']
        file = requests.get(url)
        filename = args_dict['dest'] + args_dict['filename'] + '_' +\
            args_dict['language'] + '.' + args_dict['type']

        with open(filename, 'wb') as translation_file:
            translation_file.write(file.content)
        logger.info('File %s created', filename)
    else:
        handle_error(data)


def handle_error(json: Dict):
    if json['response']['status'] == 'fail':
        raise SystemExit(json['response']['message'])
    raise SystemExit('The request was invalid, check arguments')


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    payload = build_payload(args)
    logger.info('Retrieving translations for languages %s', args.languages)
    for language in args.languages:
        process_request(payload, language)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
