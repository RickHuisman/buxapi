import unittest
from bux_api import BUXApi


class BUXApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = BUXApi()

    def test_product(self):
        expect = self.mockup_product()

        res = self.api.product(expect["securityId"])

        self.assertTrue(res["symbol"] == expect["symbol"])
        self.assertTrue(res["securityId"] == expect["securityId"])

    def test_portfolios(self):
        res = self.api.portfolios()

        self.assertTrue(isinstance(res, list))
        self.assertTrue(res[0]["totalProfitAndLoss"])

    def test_performance(self):
        res = self.api.balance()

        self.assertTrue(res["totalProfitAndLoss"])

    def test_balance(self):
        res = self.api.balance()

        self.assertTrue(res["cashBalance"])

    def test_products(self):
        expect = self.mockup_product()

        res = self.api.products()

        self.assertTrue(isinstance(res, list))
        self.assertFalse(len(res) == 0)

        symbols = [e["symbol"] for e in res]
        self.assertTrue(expect["symbol"] in symbols)

    def test_search_product(self):
        expect = self.mockup_product()

        res = self.api.search_products(expect["tagId"], expect["symbol"])

        self.assertTrue(isinstance(res, list))
        self.assertFalse(len(res) == 0)

        self.assertTrue(res[0]["symbol"] == expect["symbol"])

    def test_tags(self):
        expect = self.mockup_tag()

        res = self.api.tags()

        self.assertTrue(isinstance(res, list))
        self.assertFalse(len(res) == 0)

        self.assertTrue(expect in res)

    def test_search_user(self):
        expect = self.mockup_user()

        res = self.api.search_user(expect["nickname"])
        found_ids = [user["id"] for user in res]

        self.assertTrue(expect["id"] in found_ids)

    def test_user(self):
        expect = self.mockup_user()

        res = self.api.user(expect["id"])

        self.assertTrue(res["id"] == expect["id"])

    def test_movers(self):
        res = self.api.movers()

        self.assertTrue("bestPerformingProducts" in res)
        self.assertTrue("worstPerformingProducts" in res)
        self.assertTrue("mostTradedProducts" in res)

    def test_movers_most_traded(self):
        res = self.api.movers_most_traded()

        self.assertTrue(isinstance(res, list))
        self.assertFalse(len(res) == 0)

        self.assertTrue("symbol" in res[0])

    def test_movers_best(self):
        res = self.api.movers_best()

        self.assertTrue(isinstance(res, list))
        self.assertFalse(len(res) == 0)

        self.assertTrue("symbol" in res[0])

    def test_movers_worst(self):
        res = self.api.movers_worst()

        self.assertTrue(isinstance(res, list))
        self.assertFalse(len(res) == 0)

        self.assertTrue("symbol" in res[0])

    def test_favorite_product(self):
        expect = self.mockup_product()

        self.api.favorite_product(expect["symbol"])
        res = self.api.favorites()

        symbols = [e["symbol"] for e in res]
        self.assertTrue(expect["symbol"] in symbols)

    def test_unfavorite_product(self):
        expect = self.mockup_product()

        self.api.favorite_product(expect["symbol"])
        self.api.unfavorite_product(expect["symbol"])

        res = self.api.favorites()

        symbols = [e["symbol"] for e in res]
        print(symbols)
        self.assertFalse(expect["symbol"] in symbols)

    def test_favorites(self):
        expect = self.mockup_product()

        self.api.favorite_product(expect["symbol"])
        res = self.api.favorites()

        symbols = [e["symbol"] for e in res]
        print(symbols)
        self.assertTrue(expect["symbol"] in symbols)

    # def test_trades(self):
    #     res = self.api.trades()

    # TODO Open trade and check
    # print(res)

    # def test_open_trade(self):
    #     expect = self.mockup_product()

    #     self.api.open_trade(expect["symbol"])

    #     print(self.trades)

    # def test_close(self):
    # pass

    def mockup_product(self) -> dict:
        return {
            "symbol": "Adobe Systems",
            "securityId": "sb34799",
            "tagId": "US_STOCKS",
        }

    def mockup_tag(self) -> dict:
        return {
            "id": "US_STOCKS",
            "name": "US stocks",
        }

    def mockup_user(self) -> dict:
        return {
            "id": "f6a9c371-a792-4247-af7b-2a625baf0c96",
            "nickname": "test",
        }


if __name__ == "__main__":
    unittest.main()
