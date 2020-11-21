import os
import configparser
import requests
import json
from bux_api_config import BUXApiConfig


class BUXAccount:
    def __init__(self, email: str, password: str):
        # TODO
        """
        TODO
        """
        self.email = email
        self.password = password

    def login(self) -> str:
        """
        Get access token needed to make requests to the BUX api.

        Parameters
        ----------
        account
            Account information

        Returns
        -------
        str
            The access token for making requests to the api
        """

        credentials = {
            "credentials": {
                "email_address": self.email,
                "password": self.password,
            },
            "type": "email",
        }

        request = requests.post(
            BUXApiConfig.auth_url,
            headers=BUXApiConfig.auth_headers,
            data=json.dumps(credentials),
        )
        return request.json()["access_token"]

    @classmethod
    def get_account(cls):
        """
        Get account login infomation.

        Returns
        -------
        BUXAccount
            Account login information
        """

        email = password = ""
        if os.getenv("TRAVIS", None):
            email = os.getenv("BUX_EMAIL")
            password = os.environ.get("BUX_PASSWORD")
        else:
            config = configparser.ConfigParser()
            config.read("./config.txt")

            email = config.get("login", "email")
            password = config.get("login", "password")

        return BUXAccount(email, password)
