import json
import boto3
import logging
import os
import pprint

STREAM_NAME = 'test-datastream-dev-app-api-music-dwjp-cf'

firehose = boto3.client('firehose')
s3 = boto3.resource('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get bucket name from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key_name = event['Records'][0]['s3']['object']['key']
    
    # get bucket data from s3
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

    max_line = 1000
    if len(records) > max_line:
        # TODO : N行以上ある場合は分割したほうが良いかもしれない
        pass

    if len(records) > 0:

        try:
            _out = [{'Data': '{}'.format(record)} for record in records]

            responce_firehose = firehose.put_record_batch(
                DeliveryStreamName = STREAM_NAME,
                Records = _out
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
