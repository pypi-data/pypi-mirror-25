# -*- coding: utf-8 -*-
import requests

"""
Client Class
"""


class Client:
    """
    Constructor
    """
    def __init__(self, account, token):
        self.account = account
        self.token = token

    """
    Get url from account
    :return string
    """
    def get_url(self, endpoint=""):
        account = self.account
        default_url = "https://%s.deploybot.com/api/v1/%s"

        return default_url % (account, endpoint)

    """
    Get headers
    :return object
    """
    def get_header(self):
        token = self.token
        headers = {
            "X-Api-Token": token,
            "Accept": "application/json",
            "User-Agent": "deploybot-client agent"
        }

        return headers

    """
    Sent a GET request
    :return string
    """
    def get(self, endpoint):
        headers = self.get_header()
        url = self.get_url(endpoint)

        response = requests.get(url, headers=headers)

        return response.text

    """
    Sent a POST request
    :return string
    """
    def post(self, endpoint, params):
        headers = self.get_header()
        url = self.get_url(endpoint)
        response = requests.post(url, data=params, headers=headers)

        return response.text
