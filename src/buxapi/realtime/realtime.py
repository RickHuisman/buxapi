"""
Example subscriber usage


From BUXApi:

api = BUXApi()
events = ["portfolio.performance", "position.openend"]
api.subscribe(events, callback)

live = BUXRealTime()

"""

import asyncio
import websockets
from event import RealTimeEvent, Event


# https://stackoverflow.com/questions/1092531/event-system-in-python
class BUXRealTime:
    # TODO
    """
    Subscribe to realtime data.
    """
    def __init__(self, access_token: str):
        self.url = "wss://rtf.getbux.com/subscriptions/me"
        self.action = "portfolio.performance"
        self.access_token = access_token
        self.headers = [("Authorization", f"Bearer {access_token}")]

        self.event = Event()

        self.product = '"trading.product.sb26503"'

    async def connect(self):
        async with websockets.connect(
            self.url, extra_headers=self.headers
        ) as websocket:
            # Subscribe to product
            # await websocket.send(self.product)
            # await websocket.send(self.action)

            async for message in websocket:
                self.event(RealTimeEvent(message))

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.connect())

    def subscribe(self, callback):
        self.event.append(callback)


access_token = "eyJhbGciOiJIUzI1NiJ9.eyJyZWZyZXNoYWJsZSI6dHJ1ZSwic3ViIjoiMDA4OWFlODctNzVhZi00MWYwLTk2M2UtZTAwYzRhNGI5NjU1IiwiYXVkIjoiZ2V0YnV4LmNvbSIsInNjcCI6WyJhcHA6bG9naW4iLCJydGY6bG9naW4iLCJib3M6YXBwbGljYW50Il0sImV4cCI6MTkyMDMwODUyNywiaWF0IjoxNjA0OTQ4NTI3LCJqdGkiOiJkMWYwYTZhZS1jZDExLTRhMmYtYTRkNS04YzAwMzBkOTBhYTkiLCJjaWQiOiI4NDczNjIyOTQxIn0.ljKMDkPz7Fp7F1GroFv7irL0xPEB-23Pvsl41YtpzoU"


def test(e: RealTimeEvent):
    print(f"Event fired!: {e.event}")


class PortfolioEvent():
    def __init__(self):
        pass

#def subscribe(events, callback):


if __name__ == "__main__":
    pass
    #subscribe(["portfolio.performance"], test)

   # live = BUXRealTime(access_token)
   # subscriber.subscribe(test)
   # subscriber.start()
    # asyncio.run(main())
    # asyncio.get_event_loop().run_until_complete(subscriber.start())
