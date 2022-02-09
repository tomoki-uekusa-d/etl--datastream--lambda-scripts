#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Invalid number of arguments"
  echo "    Set <delivery-stream-name>, Check '% aws firehose list-delivery-streams'"
  exit 1
fi

DELIVERY_STREAM_NAME=$1
SCRIPT_DIR=$(cd $(dirname $0); pwd)

aws firehose describe-delivery-stream --delivery-stream-name $DELIVERY_STREAM_NAME > $SCRIPT_DIR/../src/firehose/described/$DELIVERY_STREAM_NAME.json
