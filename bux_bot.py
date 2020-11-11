import matplotlib.pyplot as plt
from bux_api import BUXApi, BUXAccount
from algo import calc_sma
import datetime

"""
Get all stock products
If not in portofolio
 If sma 50 > sma 100 this week
  Buy stock
    Print trade
Every hour print portofolio

TODO:
- Add stop loss
"""


class BUXBot:
    def __init__(self, account: BUXAccount):
        self.account = account
        self.api = BUXApi(self.account)

    def get_possible_trades(self):
        products = self.api.get_products()
        products_sma = []

        for product in products:
            stats = self.api.get_product_price_stats(product["securityId"], "1y")

            prices = [float(n["price"]) for n in stats["pricesTimeline"]]
            dates = [
                datetime.datetime.fromtimestamp(n["time"] / 1000.0)
                for n in stats["pricesTimeline"]
            ]

            products_sma.append(
                [
                    product["securityId"],
                    product["symbol"],
                    calc_sma(prices, 50),
                    calc_sma(prices, 100),
                    dates,
                ]
            )

        possible_trades = []
        for product in products_sma:
            securityId = product[0]
            symbol = product[1]
            sma50 = product[2]
            sma100 = product[3]
            dates = product[4]
            yesterday = datetime.date.today() - datetime.timedelta(days=1)

            for i, date in enumerate(dates):
                if date.date() == yesterday and sma50[i] > sma100[i]:
                    possible_trades.append([securityId, symbol, sma50[i], sma100[i]])
        return possible_trades

    def get_trades(self):
        open_trades = []
        closed_trades = []
        for trade in self.api.get_trades():
            if trade["type"] == "OPEN":
                open_trades.append(trade)
            elif trade["type"] == "CLOSE":
                closed_trades.append(trade)
        return [open_trades, closed_trades]

    def print_balance(self):
        # Cashbalance - investedAmount - totalProfitAndLoss
        print("Overview:")
        print("Cashbalance - investedAmount - totalProfitAndLoss")

    def print_status(self):
        self.print_balance()
        print("")

        trades = self.get_trades()
        close_balance = 100
        print(f"Closed trades, balance: {close_balance}:")
        self.print_trades(trades[1])
        print("")

        open_balance = 100
        print(f"Open trades: {open_balance}")
        self.print_trades(trades[0])

    def print_trades(self, trades):
        for i, trade in enumerate(trades):
            symbol = trade["product"]["symbol"]
            amount = trade["investingAmount"]["amount"]
            leverage = trade["leverage"]
            self.print_trade(i, symbol, amount, leverage)

    def print_trade(self, i, symbol, amount, leverage):
        print(f"{i+1}) {symbol} - {amount} - x{leverage}")

    def get_open_positions(self):
        positions = []
        portofolio = self.api.get_portofolio()

        positions = [p["product"]["securityId"] for p in portofolio["positions"]]
        return positions

    def start_trading(self):
        open_positions = self.get_open_positions()
        for trade in self.get_possible_trades():
            product_id = trade[0]
            if product_id not in open_positions:
                self.api.open_trade(product_id, "50", "20")
            else:
                print(f"already owned, {trade[1]}")


if __name__ == "__main__":
    api = BUXApi()
    # p = api.product('sb34799')
    p = api.movers_worst()
    print(p)

#    print(api.get_products())
#    print(api.get_product_candlesticks('sb34799', '1m'))


# bot = BUXBot()
# bot.start_trading()
# bot.print_status()


# # def get_possible_products():
# #     products = bux.get_products()
# #     products = ['sb27893']

# #     for product in products:
# #         if('INDICES' in product['tags']):
# #             symbol = product['securityId']
# #             stats = bux.get_product_price_stats(symbol, '1y')

# #             prices = [float(n['price']) for n in stats['pricesTimeline']]

# #             dates = [datetime.datetime.fromtimestamp(
# #                 n['time']/1000.0)for n in stats['pricesTimeline']]
# #             ax.plot(dates, prices)
# #             ax.plot(dates, calc_sma(prices, 20))
# #             ax.plot(dates, calc_sma(prices, 100))

# def plot_stock(symbol):
#     stats = bux.get_product_price_stats(symbol, '1y')

#     prices = [float(n['price']) for n in stats['pricesTimeline']]

#     dates = [datetime.datetime.fromtimestamp(
#         n['time']/1000.0)for n in stats['pricesTimeline']]

#     fig, ax = plt.subplots()

#     ax.plot(dates, prices, 'r-')
#     ax.plot(dates, calc_sma(prices, 50), 'g-')
#     ax.plot(dates, calc_sma(prices, 100), 'b-')

#     plt.show()


# plot_stock('sb26990')
