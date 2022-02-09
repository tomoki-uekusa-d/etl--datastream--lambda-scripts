#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Invalid number of arguments"
  echo "    Set 'bucket' 'json_path', Check '% aws s3api get-bucket-notification-configuration --bucket <TARGET_BUCKET>'"
  exit 1
fi

BUCKET=$1
JSON_PATH=$2

ABS_JSON_PATH=$(cd $(dirname $JSON_PATH); pwd)/$(basename $JSON_PATH)

echo "======================================= BEFORE ======================================="
aws s3api get-bucket-notification-configuration --bucket $BUCKET

set -eu
aws s3api put-bucket-notification-configuration --cli-input-json file://$ABS_JSON_PATH
set +eu

echo "======================================= AFTER ========================================"
aws s3api get-bucket-notification-configuration --bucket $BUCKET