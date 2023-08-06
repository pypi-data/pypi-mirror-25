# -*- coding: utf-8 -*-
from unittest import TestCase
from client.client import Client
import os


class ClientTest(TestCase):
    # Bootstrap
    def setUp(self):
        TestCase.setUp(self)

        self.account = os.environ.get('DEPLOYBOT_ACCOUNT')
        self.token = os.environ.get('DEPLOYBOT_TOKEN')
        self.client = Client(self.account, self.token)

    def test_get_url_without_parameter(self):
        self.assertRaises(TypeError, self.client.get_url())

    def test_get_url_with_endpoint_parameter(self):
        result_expected = "https://%s.deploybot.com/api/v1/%s" % (self.account, "deploy")

        self.assertEqual(result_expected, self.client.get_url("deploy"))

    def test_get_header_with_endpoint_parameter(self):
        result_expected = {
            "X-Api-Token": self.token,
            "Accept": "application/json",
            "User-Agent": "deploybot-client agent"
        }

        self.assertEqual(result_expected, self.client.get_header())

    def test_get(self):
        self.assertNotEquals("", self.client.get("users"))

    def test_post(self):
        self.assertNotEquals("", self.client.post("users", {"foo": "bar"}))
