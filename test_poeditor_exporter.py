import argparse
from unittest.mock import patch, mock_open

import pytest
import requests
import responses

import poeditorexporter


@pytest.fixture
def arg_list():
    return ['poeditorexporter', 'key0102', 'id123', 'en,fr,es',
            '/home/user/download/', 'translation', 'po']


@pytest.fixture
def arg_namespace() -> argparse.Namespace:
    p = argparse.Namespace()
    p.api_token = 'key0102'
    p.id = 'id123'
    p.languages = 'en,fr,es'
    p.dest = '/home/user/download/'
    p.filename = 'translations'
    p.type = 'po'
    return p


@pytest.fixture
def arg_dict() -> dict:
    return {'api_token': 'key0102', 'id': 'id123',
            'dest': '/home/user/download/', 'filename': 'translations',
            'type': 'po'}


@pytest.mark.parametrize('args', [
    ['poeditorexporter.py'],
    ['poeditorexporter.py', 'api121223'],
    ['poeditorexporter.py', 'api121223', 'id111'],
    ['poeditorexporter.py', 'api121223', 'id111', '/home/user/downlaod/'],
    ['poeditorexporter.py', 'api121223', 'id111', '/home/user/downlaod/',
     'translation'],
    ['poeditorexporter.py', 'api121223', 'id111', '/home/user/downlaod/',
     'translation', 'random_type'],
    ['poeditorexporter.py', 'api121223', 'id111', '/home/user/downlaod/',
     'translation', 'properties', '-f', 'no_filter']
])
def test_main_sytem_exit(args):
    with pytest.raises(SystemExit):
        poeditorexporter.main(args)


def test_parse_args(arg_list):
    args = poeditorexporter.parse_args(arg_list)

    assert type(args) is argparse.Namespace
    assert args.api_token == 'key0102'
    assert args.id == 'id123'
    assert args.languages == 'en,fr,es'
    assert args.dest == '/home/user/download/'
    assert args.filename == 'translation'
    assert args.type == 'po'


def test_build_payload(arg_namespace):
    res = poeditorexporter.build_payload(arg_namespace)

    assert res['api_token'] == 'key0102'
    assert res['id'] == 'id123'
    assert res['dest'] == '/home/user/download/'
    assert res['filename'] == 'translations'
    assert res['type'] == 'po'
    assert 'languages' not in res


def test_process_request(arg_dict):
    with patch('poeditorexporter.requests') as mock_request:
        mock_request.post.return_value = StubPostResponse()
        with patch('builtins.open', mock_open()) as mocked_file:
            poeditorexporter.process_request(arg_dict, 'fr')
            translation_file = '/home/user/download/translations_fr.po'
            mocked_file.assert_called_once_with(translation_file, 'wb')
        assert mock_request.post.call_count == 1
        assert mock_request.get.call_count == 1


@responses.activate
def test_process_request_with_response_error(arg_dict):
    responses.add(responses.POST,
                  'https://api.poeditor.com/v2/projects/export',
                  body=requests.exceptions.HTTPError())
    with pytest.raises(SystemExit):
        poeditorexporter.process_request(arg_dict, 'fr')


@responses.activate
def test_process_request_with_status_fail(arg_dict):
    responses.add(responses.POST,
                  'https://api.poeditor.com/v2/projects/export',
                  status=200,
                  json={'response':
                        {'status': 'fail', 'message': 'Invalid API Token'}
                        })
    with pytest.raises(SystemExit) as exception:
        poeditorexporter.process_request(arg_dict, 'fr')
    assert exception.type is SystemExit
    assert 'Invalid API Token' in str(exception.value)


@responses.activate
def test_main_with_filters_and_exception(arg_list: [str]):
    arg_list.extend(['-f', 'fuzzy', '-t', 'special_tags'])
    responses.add(responses.POST,
                  'https://api.poeditor.com/v2/projects/export',
                  status=200,
                  json={'response': {'status': 'error', 'message': 'Error'}})
    with pytest.raises(SystemExit) as exception:
        poeditorexporter.main(arg_list)
    assert exception.type is SystemExit
    assert 'The request was invalid, check arguments' in str(exception.value)


@responses.activate
def test_main_ok(arg_list):
    responses.add(responses.POST,
                  'https://api.poeditor.com/v2/projects/export',
                  status=200,
                  json={'response':
                        {'status': 'success', 'message': 'OK'},
                        'result':
                            {'url': 'https://api.poeditor.com/v2/' +
                                    'download/file/' +
                                    'b577a66ac39d82995debfabc016f855d'}})
    responses.add(responses.GET,
                  'https://api.poeditor.com/v2/download/' +
                  'file/b577a66ac39d82995debfabc016f855d')
    with patch('builtins.open', mock_open()):
        assert 0 == poeditorexporter.main(arg_list)

    assert responses.assert_call_count(
        'https://api.poeditor.com/v2/projects/export', 3)
    assert responses.assert_call_count(
        'https://api.poeditor.com/v2/download/file/' +
        'b577a66ac39d82995debfabc016f855d', 3)


class StubPostResponse(object):
    def __init__(self, status_code: int = 200, ok: bool = True):
        self.status_code = status_code
        self.ok = ok

    @staticmethod
    def json():
        return {
            "result": {
                "url": "https://api.poeditor.com/v2/download/file\
                    /b577a66ac39d82995debfabc016f855d"
            }
        }

    @staticmethod
    def raise_for_status():
        pass
