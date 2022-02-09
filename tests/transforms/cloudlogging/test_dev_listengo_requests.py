# -*- coding: utf-8 -*-

from unittest import TestCase

import json
import pathlib
import base64

from src.transforms.cloudlogging.dev_listengo_requests import _split, _transform, _format


class TestDevListengoRequests(TestCase):


    def test_split(self):
        abs_test_json_path = pathlib.Path('tests/resources/dev_listengo_requests_cloudlogging/test_split.json').resolve()

        with open(abs_test_json_path) as f:
            record = json.load(f)
            self.assertEqual(_split(record), record)


    def test_transform(self):
        abs_test_json_path = pathlib.Path('tests/resources/dev_listengo_requests_cloudlogging/test_transform.json').resolve()

        target_json = {
            "service_name": "dev-listengo-request",
            "log_platform": "cloudlogging",
            "time": "",
            "log_type": "",
            "facility": "",
            "client": "",
            "server": "",
            "method": "",
            "access_path": "",
            "server_port": "",
            "protocol": "",
            "protocol_version": "",
            "response_code": "",
            "user_agent": "",
            "message": ""
        }

        with open(abs_test_json_path) as f:
            record = json.load(f)
            self.assertEqual(_transform(record), record)


    def test_format(self):
        abs_test_json_path = pathlib.Path('tests/resources/dev_listengo_requests_cloudlogging/test_format.json').resolve()

        with open(abs_test_json_path) as f:
            record = json.load(f)
            self.assertEqual(_format(record), record)