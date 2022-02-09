import json
import gzip
import boto3
import logging
import urllib.parse
import os

from botocore.exceptions import ClientError

STREAM_NAME = 'datastream-prod-listengo-requests-cloudlogging'

firehose = boto3.client('firehose')
s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get bucket name from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key_name = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    
    # get bucket data from s3
    try:
        filename = object_key_name.split('/')[-1]
        tmp_file = '/tmp/{}'.format(filename)
        try:
            s3.download_file(bucket_name, object_key_name, tmp_file)
        except ClientError as e:
            raise e

        with gzip.open(tmp_file, 'rb') as f:
            file_content = f.read()
            records = [line.decode() for line in file_content.split(b'\n')]
    except Exception as e:
        print(e)
        raise e

    logger.info('Get s3 object s3://{}/{}'.format(bucket_name, object_key_name))
    logger.info('Record length: {}'.format(len(records)))

    if len(records) > 0:
        max_line = 500
        splitted_record = []
        length = len(records)
        s = max_line
        n = 0
        for r in records:
            splitted_record.append(records[n:n+s:1])
            n += s
            if n >= length:
                break

        try:
            for _records in splitted_record:
                responce_firehose = firehose.put_record_batch(
                    DeliveryStreamName = STREAM_NAME,
                    Records = [{'Data': '{}\n'.format(record)} for record in _records]
                )
        except Exception as e:
            logger.error(e)
            raise e
        logger.info(responce_firehose)
        if responce_firehose['FailedPutCount'] > 0:
            logger.error('Put Failed count'.format(responce_firehose['FailedPutCount']))
            logger.error(json.dumps(responce_firehose))
            exit(1)
        
        if len(responce_firehose['RequestResponses']) > 0:
            logger.info('Success put record.')
