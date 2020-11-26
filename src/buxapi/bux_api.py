import requests
from bux_trade import MarketOrder, LimitOrder, SellOrder
from bux_api_config import BUXApiConfig
from account.account import BUXAccount
#from subscriber.subscriber import BUXSubscriber, SubscriberEvent


class BUXApi:
    def __init__(self, account: BUXAccount = None):
        self.config = BUXApiConfig()

        if account is None:
            account = BUXAccount.get_account()

        self.access_token = account.login()

    def query(self, query: str) -> str:
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        request = requests.get(url, headers=headers)
        return request.json()

    def query_with_data(self, query: str, data: dict) -> str:
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        request = requests.get(url, headers=headers, params=data)
        return request.json()

    def stats_query_with_data(self, query: str, data: dict) -> str:
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = "https://api.getbux.com/stats/2/graph/" + query
        request = requests.get(url, headers=headers, params=data)
        return request.json()

    def put(self, query: str):
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        requests.put(url, headers=headers)

    def put_with_data(self, query: str, data: dict):
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        request = requests.put(url, json=data, headers=headers)
        print(request.json())

    def delete(self, query: str):
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
        request = requests.delete(url, headers=headers)
        print(request)
        print(request.json())

    def post(self, query: str, data: dict) -> str:
        headers = BUXApiConfig.get_bearer_headers(self.access_token)

        url = BUXApiConfig.base_endpoint_url + query
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

    def news_item(self, item_id: str) -> dict:
        """
        Get news item.

        Parameters
        ----------
        item_id : str
            The id of the news item

        Returns
        -------
        dict
            A dict containing news item
        """

        return self.query(f"users/me/news/{item_id}")

    def product_news(self, product_id: str) -> dict:
        """
        Get news items about product.

        Parameters
        ----------
        product_id : str
            The id of the product

        Returns
        -------
        dict
            A dict with news items
        """

        return self.query(f"products/{product_id}/news")

    def feed(self) -> dict:
        """
        TODO

        Returns
        -------
        """

        return self.query("users/me/socialfeed")

    def fee_schedules(self, product_id: str) -> dict:
        """
        Get trading fees.

        Returns
        -------
        dict
            A dict containing trading fees
        """

        return self.query(f"/users/me/products/{product_id}/fee-schedules")

    def curated_products(self) -> list:
        """
        Get curated products.

        Returns
        -------
        list
            A list of curated products
        """

        return self.query(f"/products")

    """
    TODO
    setProductPriceTracker
    deleteProductPriceTracker
    fetchTradeConfiguration
    """

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
            A dict of the best performing, worst performing and
            most traded products
        """
        return self.query("movers")

    def movers_most_traded(self) -> dict:
        """
        Get the most traded products.

        Returns
        -------
        list
            A list of the most traded products
        """

        return self.query("movers/mostTraded")

    def movers_best(self) -> dict:
        """
        Get the best performing products.

        Returns
        -------
        list
            A list of the best performing products
        """

        return self.query("movers/mostTraded")

    def movers_worst(self) -> dict:
        """
        Get the worst performing products.

        Returns
        -------
        list
            A list of the worst performing products
        """

        return self.query("movers/worst")

    def product(self, product_id: str) -> dict:
        """
        Get a product detail by id.

        Parameters
        ----------
        product_id : str
            The id of the product

        Returns
        -------
        dict
            A dict containing product detail
        """

        return self.query(f"products/{product_id}")

    def product_alert(self, product_id: str, amount: int):
        """
        Set a product alert.

        Parameters
        ----------
        TODO
        """

        data = {
            "limit": {
                "amount": str(amount),
                "decimals": "2",
                # upper or lower??? PortfolioRetrofitService.smali line 397: value = "trackerTypeMode"
                # TODO "decimals": (amount.split('.')[1] || []).length}}
            }
        }

        self.put_with_data(f"users/me/products/{product_id}/tracker", data)

    def delete_product_alert(self, product_id: str):
        """
        Delete a product alert.

        Parameters
        ----------
        product_id : str
            The id of a product an alert has been set on
        """

        return self.delete(f"users/me/products/{product_id}/tracker")

    def position_alert(self, position_id: str):
        """
        TODO
        """

        data = {

        }

        trackerTypeMode = "upperLimit" # ???

        self.put_with_data(
            f"users/me/portfolio/positions/{position_id}/{trackerTypeMode}",
            data
        )

    def delete_position_alert(self, position_id: str):
        """
        TODO
        """

        pass

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
            A list of all products
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
            A list of products
        """

        return self.query_with_data(
            "products/search", {"tagId": tag_id, "q": search_term}
        )

    def tags(self) -> list:
        """
        Get product tags.

        Returns
        ----------
        list
            A list of all product tags
        """

        return self.query("products/tags")

    def trade_configuration(self, product_id: str) -> dict:
        """
        Get trade configuration for product

        Parameters
        ----------
        product_id : str
            The id of the product

        Returns
        -------
            A dict containing trade configuration
        """

        return self.query(f"users/me/tradeconfigurations/{product_id}")

    def search_user(self, query: str) -> list:
        """
        Search for user.

        Parameters
        ----------
        query : str
            The search query

        Returns
        -------
        list
            A list of users
        """
        return self.query_with_data("search/people/", {"q": query})

    def user(self, user_id: str) -> dict:
        """
        Get user by id.

        Parameters
        ----------
        user_id : str
            The id of the user

        Returns
        -------
        dict
            A dict containing user info
        """

        return self.query(f"/users/{user_id}/profile")

    def notifications(self) -> list:
        """
        Get pending notifications.

        Returns
        -------
        list
            A list of pending notifications
        """
        return self.query("/users/me/notifications")

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
        Get trades history of logged in user.

        Returns
        -------
        list
            A list of all trades
        """

        return self.query("/users/me/trades")

    def place_market_order(self, order: MarketOrder):
        """
        Execute order at the current market price.

        Parameters
        ----------
        order : MarketOrder
            The order to execute
        """

        self.post("/users/me/portfolio/market-orders", order.to_dict())

    def place_limit_order(self, order: LimitOrder):
        """
        Execute order at target price.

        Parameters
        ----------
        order : LimitOrder
            The order to execute
        """

        self.post("/users/me/portfolio/limit-orders", order.to_dict())

    def get_autoclose_limit_order(self, order_id: str):
        """
        Get current and allowed autoclose configuration for a limit order.

        Parameters
        ----------
        order_id : int
            The id of the order
        """

        return self.query(
            f"/users/me/portfolio/limit-orders/{order_id}/automaticExecutionTracker"
        )

    def autoclose_limit_order(
        self, order_id: str, lower_limit: float, upper_limit: float
    ):
        """
        Automatically close position when it reaches a certain limit.
        Limits are percentages so lower_limit = -0.1 == -10%

        Parameters
        ----------
        order_id : int
            The id of the order
        lower_limit : float
            The lower limit of the autoclose (in %).
        upper_limit : float
            The upper limit of the autoclose (in %).
        """

        data = {"lowerLimit": lower_limit, "upperLimit": upper_limit}

        self.put_with_data(
            f"/users/me/portfolio/limit-orders/{order_id}/automaticExecutionTracker",
            data,
        )

    def get_autoclose_position(
        self, position_id: str
    ):
        """
        Get current and allowed autoclose configuration for a position.

        Parameters
        ----------
        position_id : str
            The id of the position
        """

        return self.query(
            f"/users/me/portfolio/positions/{position_id}/automaticExecutionTracker",
        )

    def autoclose_position(
        self, position_id: str, upper_limit: float, lower_limit: float
    ):
        # TODO not working...
        """
        TODO
            #"lowerLimitPrice": lower_limit,
            #"upperLimitPrice": lower_limit,
            # "upperLimit": 5,
            # "lowerLimit": 25,

            #"lowerLimit": 25.000,
            #"upperLimit": 0.029,

        e.g.:
        "upperLimit": 0.8,
        "lowerLimit": -0.10,
        """

        data = {
            "upperLimit": upper_limit,
            "lowerLimit": lower_limit,
        }

        self.put_with_data(
            f"/users/me/portfolio/positions/{position_id}/automaticExecutionTracker",
            data
        )

    def delete_autoclose_limit_order(
        self, order_id: str
    ):
        """
        Delete autoclose from order.

        Parameters
        ----------
        order_id : int
            The id of the order
        """

        self.delete(
            f"/users/me/portfolio/limit-orders/{order_id}/automaticExecutionTracker",
        )

    def delete_autoclose_position(
        self, position_id: str
    ):
        """
        Delete autoclose from position.

        Parameters
        ----------
        position_id : int
            The id of the position
        """

        self.delete(
            f"/users/me/portfolio/positions/{position_id}/automaticExecutionTracker"
        )

    def close(self, position_id: str):
        """
        Close a position.

        Parameters
        ----------
        position_id : str
            The id of the position to close
        """

        self.delete(f"/users/me/portfolio/positions/{position_id}")

    def limit_order(self, order_id: str) -> dict:
        """
        Get limit order information.

        Parameters
        ----------
        order_id : str
            The id of the order

        Returns
        -------
        dict
            A dict containing information about the order
        """

        return self.query(f"/users/me/portfolio/limit-orders/{order_id}")

    def position(self, position_id: str) -> dict:
        """
        Get position information.

        Parameters
        ----------
        position_id : str
            The id of the position

        Returns
        -------
        dict
            A dict containing information about the position
        """

        return self.query(f"/users/me/portfolio/positions/{position_id}")


    def subscribe(self, events, callback):
        # TODO Blocking
        # TODO Strong typing
        subscriber = BUXSubscriber(self.access_token)
        subscriber.subscribe(callback)
        subscriber.start()

    def position_note(self, position_id: str) -> str:
        """
        Get note on position.

        Parameters
        ----------
        position_id : str
            The id of the position

        Returns
        -------
        str
            A string containing a note
        """

        return self.query(f"/users/me/portfolio/positions/{position_id}/note")

    def save_position_note(self, position_id: str, note: str) -> str:
        """
        TODO
        """

        return self.put_with_data(
            f"/users/me/portfolio/positions/{position_id}/note", note
        )

    def set_multiplier(self, position_id: str, multiplier: str):
        """
        Set multiplier on position.

        Parameters
        ----------
        position_id : str
            The id of the position
        mutliplier : str
            The new multiplier for the position
        """

        data = { "newMultiplier": multiplier }

        self.put_with_data(
            f"users/me/portfolio/positions/{position_id}/leverage",
            data
        )


    def flexible_multiplier_configurations(self, position_id: str):
        """
        TODO

        Returns:
        [{'investedAmount': {'currency': 'BUX', 'decimals': 2, 'amount': '50.00'},
        'leverage': 1, 'notionalValue': {'currency': 'BUX', 'decimals': 2, 'amount': '50.00'},
        'availableCashForTrading': {'currency': 'BUX', 'decimals': 2, 'amount': '1081.20'}, 'allowed': True}]
        """

        return self.query(
            f"users/me/portfolio/positions/{position_id}/flexiblemultiplierconfigurations",
        )

"""
TODO

cancelLimitOrderDeferred
checkWithdrawalAmount

collapse
expand
mov
setPositionTracker ???
fetchPositionTracker
fetchFlexibleMultiplierConfigurations ???
"""

# def f(x: SubscriberEvent):
# print(x)

api = BUXApi()
#print(api.position("04c46d11-95db-42c7-9105-a48e82e2c19e"))
api.position_alert("04c46d11-95db-42c7-9105-a48e82e2c19e")
#print(api.flexible_multiplier_configurations("04c46d11-95db-42c7-9105-a48e82e2c19e"))
#print(api.get_autoclose_limit_order("fdb7bcbf-2c80-4c9c-a689-63c755021400"))
#print(api.get_autoclose_market_order("04c46d11-95db-42c7-9105-a48e82e2c19e"))

#print(api.portfolios()[0])
#for p in api.portfolios()[0]["positions"]:
     #print(p)
     #print("")

# api.autoclose_market_order("04c46d11-95db-42c7-9105-a48e82e2c19e", -0.1, 0.5)
#api.delete_autoclose_market_order("04c46d11-95db-42c7-9105-a48e82e2c19e")

#print(api.limit_order("fdb7bcbf-2c80-4c9c-a689-63c755021400"))
#api.autoclose_limit_order("fdb7bcbf-2c80-4c9c-a689-63c755021400", -0.1, 0.5)
#api.delete_autoclose_limit_order("fdb7bcbf-2c80-4c9c-a689-63c755021400")
