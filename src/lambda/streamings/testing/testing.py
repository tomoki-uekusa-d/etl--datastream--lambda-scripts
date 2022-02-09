# -*- coding: utf-8 -*-

import json
import gzip
import boto3
import logging
import os
import pprint
import urllib.parse

from botocore.exceptions import ClientError

STREAM_NAME = 'test-datastream-testing'

firehose = boto3.client('firehose')
s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    pprint.pprint(event)
    # get bucket name from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key_name = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    print('s3_path: {}/{}'.format(bucket_name, object_key_name))
    
    # get bucket data from s3
    try:
        filename = object_key_name.split('/')[-1]
        print('filename: {}'.format(filename))
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

    max_line = 1000
    if len(records) > max_line:
        # TODO : N行以上ある場合は分割したほうが良いかもしれない
        pass

    if len(records) > 0:

        try:
            responce_firehose = firehose.put_record_batch(
                DeliveryStreamName = STREAM_NAME,
                Records = [{'Data': '{}\n'.format(record)} for record in records]
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
