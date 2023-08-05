from pydash import _
from app.services.mock_service import Mock

def tranpose(data):
    reqs = list()
    for request in data['requests']:
        response = request['responses'][0] if len(request['responses']) > 0 else {
            'status': '200',
            'headers': [],
            'text': ''
        };
        reqs.append(Mock(
            req={
                'url': request['url'],
                'method': request['method'],
                'headers': transpose_req_headers(request['headers']),
                'body': request['rawModeData'] if 'rawModeData' in request else ''
            },
            res={
                'status': response['status'],
                'headers': transpose_res_headers(response['headers']),
                'body': response['text'][:len(response['text']) - 1]
            }
        ))
    return reqs

def transpose_req_headers(headers_str):
    headers = {}
    for header in headers_str.split('\n'):
        try:
            headers[header[:header.index(': ')]] = header[header.index(': ') + 2:]
        except ValueError:
            pass
    return headers

def transpose_res_headers(headers_arr):
    headers = {}
    for header in headers_arr:
        headers[header['key']] = header['value']
    return headers
