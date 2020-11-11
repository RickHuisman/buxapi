import os
import configparser
import requests
import json
from bux_api_config import BUXApiConfig


class BUXAccount:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class BUXApi:
    def __init__(self, account: BUXAccount = None):
        self.config = BUXApiConfig()

        if account is None:
            account = self.get_account()

        self.access_token = self.login(account)

    def get_account(self) -> BUXAccount:
        """
        Get account login infomation.

        Returns
        -------
        BUXAccount
            Account login information
        """

        if os.getenv('TRAVIS', None):
            email = os.getenv('BUX_EMAIL')
            password = os.environ.get('BUX_PASSWORD')

            return BUXAccount(email, password)
        else:
            config = configparser.ConfigParser()
            config.read("./config.txt")

            email = config.get("login", "email")
            password = config.get("login", "password")

            return BUXAccount(email, password)

    def login(self, account: BUXAccount) -> str:
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
                "email_address": account.email,
                "password": account.password,
            },
            "type": "email",
        }

        request = requests.post(
            BUXApiConfig.auth_url,
            headers=self.config.auth_headers,
            data=json.dumps(credentials),
        )
        return request.json()["access_token"]

    def query(self, query: str) -> str:
        headers = self.config.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        request = requests.get(url, headers=headers)
        return request.json()

    def query_with_data(self, query: str, data: dict) -> str:
        headers = self.config.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        request = requests.get(url, headers=headers, params=data)
        return request.json()

    def stats_query_with_data(self, query: str, data: dict) -> str:
        headers = self.config.get_bearer_headers(self.access_token)

        url = "https://api.getbux.com/stats/2/graph/" + query
        request = requests.get(url, headers=headers, params=data)
        return request.json()

    def put(self, query: str):
        headers = self.config.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        requests.put(url, headers=headers)

    def delete(self, query: str):
        headers = self.config.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        requests.delete(url, headers=headers)

    def post(self, data):
        headers = self.config.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + "users/me/trades"
        request = requests.post(url, json=data, headers=headers)
        return request.json()

    def favorites(self) -> list:
        """
        Get all products that are marked as favorite.

        Returns
        -------
        list
            Favorite products
        """

        return self.query("products/favorites")

    def favorite_product(self, symbol_id: str):
        """
        Mark a product as favorite.

        Parameters
        ----------
        symbol_id:
            The id of the product
        """

        self.put(f"products/favorites/{symbol_id}")

    def unfavorite_product(self, symbol_id: str):
        """
        Unmark a product as favorite.

        Parameters
        ----------
        symbol_id:
            The id of the product
        """

        self.delete(f"products/favorites/{symbol_id}")

    def movers(self) -> dict:
        """
        Get the best performing, worst performing and most traded products.

        Returns
        -------
        dict
            The best performing, worst performing and most traded products
        """
        return self.query("movers")

    def movers_most_traded(self) -> dict:
        """
        Get the most traded products.

        Returns
        -------
        list
            The most traded products
        """

        return self.query("movers/mostTraded")

    def movers_best(self) -> dict:
        """
        Get the best performing products.

        Returns
        -------
        list
            The best performing products
        """

        return self.query("movers/mostTraded")

    def movers_worst(self) -> dict:
        """
        Get the worst performing products.

        Returns
        -------
        list
            The worst performing products
        """

        return self.query("movers/worst")

    def product(self, product_id: str) -> dict:
        """
        Get a product by id.

        Parameters
        ----------
        product_id : str
            The id of the product

        Returns
        -------
        dict
            The product
        """

        return self.query(f"products/{product_id}")

    def product_candlesticks(self, product_id: str, type: str) -> list:
        return self.stats_query_with_data(
            f"products/{product_id}/candlestick", {"type": type}
        )

    def product_price_stats(self, product_id: str, type: str):
        return self.stats_query_with_data(
            f"products/{product_id}/price", {"type": type}
        )

    def products(self) -> dict:
        """
        Get all products.

        Returns
        -------
        list
            All products
        """

        return self.query("products/search")

    def search_products(self, tag_id: str, search_term: str) -> list:
        """
        Search for products by tag and symbol.

        Parameters
        ----------
        tag_id: str
            The tag id of the product
        search_term: str
            The symbol of the product to search for

        Returns
        -------
        list
            Products matching search term
        """

        return self.query_with_data(
            "products/search", {"tagId": tag_id, "q": search_term}
        )

    def set_product_price_tracker(self):
        pass

    def delete_product_price_tracker(self):
        pass

    def tags(self) -> list:
        """
        Get product tags.

        Returns
        ----------
        list
            All product tags
        """

        return self.query("products/tags")

    def trade_configuration(self, product_id: str) -> dict:
        return self.query(f"users/me/tradeconfigurations/{product_id}")

    def portfolio(self) -> dict:
        """Get portfolio of logged in user.
        :TODO
        """

        return self.query("/users/me/portfolio")

    def trades(self) -> list:
        """
        Get trades of logged in user.

        Returns
        -------
        list
            Open trades
        """

        return self.query("/users/me/trades")

    # TODO Strong typing
    def open_trade(self, symbol_id: str, amount, leverage):
        """"""

        data = {
            "productId": product_id,
            "investingAmount": {"currency": "BUX", "decimals": "2", "amount": amount},
            "leverage": 1,
            "direction": "BUY",
        }
        return self.post(data)

    def fee_schedules(self):
        pass


# buxApi = BUXApi(account)
# # print(type(buxApi.get_product('sb34799')))
# print(type(buxApi.get_product_candlesticks('sb34799', '1m')))
# print(buxApi.search_products('NL_STOCKS', 'ASML'))
# print(type(buxApi.get_trade_configuration('sb34799')))
