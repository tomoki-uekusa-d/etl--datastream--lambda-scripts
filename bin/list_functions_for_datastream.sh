#!/bin/bash

aws lambda list-functions | python -m json.tool | grep 'FunctionName' | grep -i datastream | awk '{print $NF}' | sed -e 's/"//g' -e 's/,//g'
