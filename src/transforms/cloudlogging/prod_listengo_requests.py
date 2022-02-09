# -*- coding: utf-8 -*-

import json
import base64
import re
import pprint
import datetime

SERVICE_NAME='prod-listengo-requests'
LOG_PLATFORM='cloudlogging'


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
    return json.loads(data)


# check following links
# https://cloud.google.com/logging/docs/structured-logging
# https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
def _transform(data):
    _out = {}

    _out['service_name'] = SERVICE_NAME
    _out['log_platform'] = LOG_PLATFORM
    _out['time'] = '{}'.format(_format_time(data.get('receiveTimestamp', '')))
    _out['log_type'] = data.get('resource', {}).get('type', '')
    _out['facility'] = _check_facility(data.get('severity', ''))

    httpRequest = data.get('httpRequest', {})
    _out['client'] = httpRequest.get('remoteIp', '')
    _out['server'] = httpRequest.get('serverIp', '')
    _out['method'] = httpRequest.get('requestMethod', '')
    _out['access_path'] = _format_access_path(httpRequest.get('requestUrl', ''))
    _out['server_port'] = _format_server_port(httpRequest.get('requestUrl', ''))
    _out['protocol'] = _format_protocol(httpRequest.get('requestUrl', ''))
    _out['protocol_version'] = httpRequest.get('protocol', '')
    _out['response_code'] = str(httpRequest.get('status', ''))
    _out['user_agent'] = httpRequest.get('userAgent', '')
    _out['message'] = ''

    return _out


def _format(data):
    return data


def _check_facility(data):
    if data == 'CRITICAL':
        return 'critial'
    elif data == 'EMERGENCY':
        return 'fatal'
    elif data in ['ERROR', 'ALERT']:
        return 'error'
    elif data == 'WARNING':
        return 'warning'
    elif data in ['INFO', 'DEFAULT', 'DEBUG', 'NOTICE']:
        return 'info'


def _format_time(data):
    mg = re.match(r'^(.*)\.([0-9]+)Z$', data).groups()
    fmt_str = "{}.{}".format(mg[0], mg[1][:-3])
    dd = datetime.datetime.strptime(fmt_str, "%Y-%m-%dT%H:%M:%S.%f")
    return dd.strftime("%Y-%m-%d %H:%M:%S")


def _format_access_path(data):
    m = re.match(r'(.*)://(.*)$' , data)
    return '/' + '/'.join(m.groups()[1].split('/')[1:])


def _format_server_port(data):
    m = re.match(r'(.*)://(.*)$' , data)
    protocol = m.groups()[0]
    host_port = m.groups()[1].split('/')[0]
    m2 = re.match(r'(.*):([0-9]+)', host_port)
    port = m2.groups()[1] if m2 else ''
    
    if port != '':
        return int(port)
    elif protocol == 'http':
        return 80
    elif protocol == 'https':
        return 443
    else:
        return ''

def _format_protocol(data):
    m = re.match(r'(.*)://(.*)$' , data)
    return m.groups()[0]
