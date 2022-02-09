#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Invalid number of arguments"
  echo "    Set <delivery-stream-name>, Check '% aws firehose list-delivery-streams'"
  exit 1
fi

DELIVERY_STREAM_NAME=$1

set -eu

aws firehose delete-delivery-stream --delivery-stream-name $DELIVERY_STREAM_NAME

set +e

printf "'$DELIVERY_STREAM_NAME' is in Deleting queue ..."

while true
do
  RESULT=$(aws firehose list-delivery-streams | grep -c $DELIVERY_STREAM_NAME)
  if [ "$RESULT" == "0" ]; then
    break
  fi
  printf "."
  sleep 3
done

printf " DONE!!!\n"
