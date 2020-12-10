import json
import urllib.request
import boto3
import logging
import pprint
from datetime import datetime

SLACK_URL = "https://hooks.slack.com/services/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"

s3 = boto3.resource('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get bucket name from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key_name = event['Records'][0]['s3']['object']['key']

    records = get_bucket_data(bucket_name, object_key_name)
    notification_data = create_notification_data(records)
    post_slack(post_data=notification_data)


def get_bucket_data(bucket_name, object_key_name):
    try:
        obj = s3.Object(bucket_name, object_key_name) 
        response = obj.get()
        body = response['Body'].read()
        records = body.decode('utf-8').splitlines()
    except Exception as e:
        logger.error(e)
        raise e

    logger.info('Get s3 object s3://{}/{}'.format(bucket_name, object_key_name))
    logger.info('Record length: {}'.format(len(records)))

    return records


def create_notification_data(records):
    _color = None
    _attachments = []

    for line in records:
        d = json.loads(line, strict=False)

        title = "{time}\t{facility}\t{method}\t{access_path}".format(
            time = d['time'],
            facility=d['facility'].upper(),
            method = d['method'],
            access_path = d['access_path']
        )
        value = "{response_code}\t{message}".format(
            server = d['server'],
            response_code = d['response_code'],
            message = d['message']
        )

        if d['facility'] == 'error':
            _color = 'danger'
        elif d['facility'] == 'warning':
            _color = 'warning'
        elif d['facility'] == 'info' and d['response_code'].startswith('2'):
            _color = 'good'
        else:
            _color = None


        _attachments.append({
            "color": _color,
            "fields": [{
                'title': title,
                'value': value
            }],
            "footer": 'Server: {}{}\tClient: {}\tService: {}\tLogType: {}'.format(
                d['server'],
                ':{}'.format(d['server_port']),
                d['client'],
                d['service_name'],
                d['log_platform']
            ),
            "ts": int(datetime.strptime(d['time'], '%Y-%m-%d %H:%M:%S').timestamp())
        })

    send_data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*ログ統合基盤からの通知(テスト)*"
                }
            }
        ],
        "attachments": _attachments
    }

    return json.dumps(send_data)


def post_slack(post_data):
    request = urllib.request.Request(
        SLACK_URL, 
        data=post_data.encode('utf-8'), 
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
