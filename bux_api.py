import os
import configparser
import requests
import json
from bux_api_config import BUXApiConfig
from subscriber import BUXSubscriber, SubscriberEvent


class BUXTrade:
    def __init__(self, product_id: str, amount: int, multiplier: int):
        self.product_id = product_id
        self.amount = amount
        self.multiplier = multiplier
        self.direction = "BUY"


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

        TODO

        Returns
        -------
        BUXAccount
            Account login information
        """

        if os.getenv("TRAVIS", None):
            email = os.getenv("BUX_EMAIL")
            password = os.environ.get("BUX_PASSWORD")

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

    def news(self) -> dict:
        """
        Get news articles.

        Returns
        -------
        dict
            A dict of news articles
        """

        return self.query("users/me/news")

    def feed(self) -> dict:
        """
        TODO

        Returns
        -------
        """

        return self.query("users/me/socialfeed")

    def fees(self) -> dict:
        """
        TODO

        Returns
        -------
        """

        return self.query("users/me/feeschedule")

    def favorites(self) -> list:
        """
        Get all products that are marked as favorite.

        Returns
        -------
        list
            A list of favorite products
        """

        return self.query("products/favorites")

    def favorite_product(self, symbol_id: str):
        """
        Mark a product as favorite.

        Parameters
        ----------
        symbol_id: str
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

    def product_candlestick(self, product_id: str, timespan: str) -> list:
        """
        Get price history of product.

        Parameters
        ----------
        product_id : str
            The id of the product
        timespan : str
            TODO
            Possible timespans: ['1d', '5d', '1M', '3M', '6M', '1Y']

        Returns
        -------
        dict
            TODO
        """

        return self.stats_query_with_data(
            f"products/{product_id}/candlestick", {"type": timespan}
        )

    def product_price(self, product_id: str, timespan: str) -> dict:
        """
        Get price history of product.

        Parameters
        ----------
        product_id : str
            The id of the product
        timespan : str
            TODO
            Possible timespans: ['1d', '5d', '1M', '3M', '6M', '1Y']

        Returns
        -------
        dict
            TODO
        """

        return self.stats_query_with_data(
            f"products/{product_id}/price", {"type": timespan}
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

    def portfolios(self) -> list:
        """
        Get portfolios.

        Returns
        -------
        list
            A list of portofolios
        """

        return self.query("/users/me/portfolios")

    def performance(self) -> dict:
        """
        Get performance of portfolio.

        Returns
        -------
        dict
            A dict with perfomance info about portfolio
        """

        return self.query("/users/me/portfolio/performance")

    def balance(self) -> dict:
        """
        Get cash balance.

        Returns
        -------
        dict
            A dict with balance info about portfolio
        """

        return self.query("/users/me/portfolio/cashBalance")

    def trades(self) -> list:
        """
        Get trades of logged in user.

        Returns
        -------
        list
            Open trades
        """

        return self.query("/users/me/trades")

    def trade(self, trade: BUXTrade) -> str:
        """
        Open a trade.

        Parameters
        ----------


        Returns
        -------
        """

        data = {
            "productId": trade.product_id,
            "investingAmount": {
                "currency": "BUX",
                "decimals": "2",
                "amount": trade.amount,
            },
            "leverage": trade.multiplier,
            "direction": trade.direction,
        }
        return self.post(data)

    def close(self):
        pass

    def fee_schedules(self):
        pass

    def subscribe(self, events, callback):
        # TODO Blocking
        # TODO Strong typing
        subscriber = BUXSubscriber(self.access_token)
        subscriber.subscribe(callback)
        subscriber.start()


#def f(x: SubscriberEvent):
    #print(x)


#api = BUXApi()
#res = api.product_candlestick('sb34799', '1d')
#res = api.product_price_stats('sb34799')
#res = api.performance()
#print(res)
#print(api.performance())
#print(api.balance())
#api.subscribe(['portfolio.performance'], f)

# # print(type(buxApi.get_product('sb34799')))
# print(type(buxApi.get_product_candlesticks('sb34799', '1m')))
# print(buxApi.search_products('NL_STOCKS', 'ASML'))
# print(type(buxApi.get_trade_configuration('sb34799')))
