# TODO Add documentation
class OrderDirection:
    def __init__(self, repr: str):
        self.repr = repr

    def __repr__(self) -> str:
        return self.repr


class BuyOrder(OrderDirection):
    def __init__(self):
        super().__init__("BUY")


class SellOrder(OrderDirection):
    def __init__(self):
        super().__init__("SELL")


class BUXOrder:
    def __init__(
        self, product_id: str, amount: int, leverage: int, direction: OrderDirection
    ):
        self.product_id = product_id
        self.amount = amount
        self.leverage = leverage
        self.direction = direction


class MarketOrder(BUXOrder):
    def __init__(
        self,
        product_id: str,
        amount: int,
        leverage: int,
        direction: OrderDirection,
    ):
        super().__init__(product_id, amount, leverage, direction)

    def to_dict(self) -> dict:
        return {
            "productId": self.product_id,
            "direction": repr(self.direction),
            "investingAmount": {
                "currency": "BUX",
                "decimals": "2",  # TODO
                "amount": self.amount,
            },
            "leverage": self.leverage,
        }


class LimitOrder(BUXOrder):
    def __init__(
        self,
        product_id: str,
        amount: int,
        leverage: int,
        direction: OrderDirection,
        target_price: int,
    ):
        super().__init__(product_id, amount, leverage, direction)
        self.target_price = target_price

    def to_dict(self) -> dict:
        return {
            "productId": self.product_id,
            "direction": repr(self.direction),
            "investingAmount": {
                "currency": "BUX",
                "decimals": 2,  # TODO
                "amount": self.amount,
            },
            "leverage": self.leverage,
            "targetPrice": 0.9,
        }


# class LimitOrderAutomaticExecution():
#    def __init__(self):
#        pass
