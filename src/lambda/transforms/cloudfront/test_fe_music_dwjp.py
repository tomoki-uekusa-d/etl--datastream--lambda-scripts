# -*- coding: utf-8 -*-

import json
import base64
import re
import pprint

SERVICE_NAME='dev-app-api-music.dwango.jp'
LOG_PLATFORM='cloudfront'

def lambda_handler(event, context):
    output = []
    
    for record in event['records']:
        data = base64.b64decode(record['data']).decode('utf-8')

        if not re.match('^(#.*|\n$)', data):
            splitted = _split(data)
            transformed = _transform(splitted)
            formatted = _format(transformed)
            formatted['org_body'] = data
            output.append({
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(json.dumps(formatted).encode() + "\n".encode()).decode()
            })
        else:
            formatted = ''
            output.append({
                'recordId': record['recordId'],
                'result': 'Dropped',
                'data': '',
            })
    pprint.pprint(output)
        
    return { 'records': output }


def _split(data):
    data_format = [
        "date",
        "time",
        "x-edge-location",
        "sc-bytes",
        "c-ip",
        "cs-method",
        "cs(Host)",
        "cs-uri-stem",
        "sc-status",
        "cs(Referer)",
        "cs(User-Agent)",
        "cs-uri-query",
        "cs(Cookie)",
        "x-edge-result-type",
        "x-edge-request-id",
        "x-host-header",
        "cs-protocol",
        "cs-bytes",
        "time-taken",
        "x-forwarded-for",
        "ssl-protocol",
        "ssl-cipher",
        "x-edge-response-result-type",
        "cs-protocol-version",
        "fle-status",
        "fle-encrypted-fields",
        "c-port",
        "time-to-first-byte",
        "x-edge-detailed-result-type",
        "sc-content-type",
        "sc-content-len",
        "sc-range-start",
        "sc-range-end"
    ]
    splitted = data.split("\t")
    _dict = {key: val for key, val in zip(data_format, splitted)}
    return _dict

def _transform(data):
    _out = {}

    _out['service_name'] = SERVICE_NAME
    _out['log_platform'] = LOG_PLATFORM
    _out['time'] = '{} {}'.format(data['date'], data['time'])
    _out['log_type'] = data['x-edge-response-result-type']
    _out['facility'] = _check_facility(data['sc-status'])
    _out['client'] = data['c-ip']
    _out['server'] = data['x-host-header']
    _out['method'] = data['cs-method']
    _out['access_path'] = data['cs-uri-stem']
    _out['server_port'] = _check_port(data['cs-protocol'])
    _out['protocol'] = data['cs-protocol']
    _out['protocol_version'] = data['cs-protocol-version']
    _out['response_code'] = data['sc-status']
    _out['user_agent'] = data['cs(User-Agent)']
    _out['message'] = ''

    return _out


def _format(data):
    return data

def _check_facility(data):
    if data.startswith('2'):
        return 'info'
    elif data.startswith('4'):
        return 'warning'
    elif data.startswith('5'):
        return 'error'
    else:
        return 'info'

def _check_port(data):
    if data == 'https' or data == 'wss':
        return 443
    elif data == 'http' or data == 'ws':
        return 80
    else:
        return data