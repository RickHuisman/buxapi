from dataclasses import dataclass


@dataclass
class BUXApiConfig:
    """Configuration for the BUX api.

    Attributes:
        api_version: The version of the BUX api.
        auth_token: The auth token used in the header.
        auth_url: The url used to fetch access_tokens for an account.
        base_endpoint_url: The base endpoint url used for the api.
        auth_headers: The headers necessary for fetching access_tokens.
        headers: The headers necessary for makin requests to the bux api.
    """

    api_version = "25"
    auth_token = "ODQ3MzYyMjk0MTpFSkFjb3V3RkdnVlpNVVpHZVJXNg=="
    auth_url = "https://api.getbux.com/auth/3/authorize"
    base_endpoint_url = "https://api.getbux.com/core/" + api_version + "/"
    auth_headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Basic " + auth_token,
    }

    def get_bearer_headers(self, access_token: str) -> dict:
        """Get the headers necessary for making requests to the bux api.
        :param  access_token TODO
        :returns dictionary containing request headers
        """
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + access_token,
        }
