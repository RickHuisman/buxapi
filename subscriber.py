import asyncio
import websockets
from event import SubscriberEvent, Event


class BUXSubscriber:
    def __init__(self, access_token: str):
        self.url = 'wss://rtf.getbux.com/subscriptions/me'
        self.action = 'portfolio.performance'
        self.access_token = access_token
        self.headers = [('Authorization', f'Bearer {access_token}')]

        self.event = Event()

        self.product = 'product.sb26500'

    async def connect(self):
        async with websockets.connect(self.url, extra_headers=self.headers) as websocket:
            # Subscribe to product
            # await websocket.send(product)
            await websocket.send(self.action)

            async for message in websocket:
                self.event(SubscriberEvent(message))

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.connect())

    def subscribe(self, callback):
        self.event.append(callback)


async def fibonacci(nterms):
    n1, n2 = 0, 1
    count = 0

    # check if the number of terms is valid
    if nterms <= 0:
        print("Please enter a positive integer")
    elif nterms == 1:
        print("Fibonacci sequence upto", nterms, ":")
        print(n1)
    else:
        while count < nterms:
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth
            count += 1
    print(f"Completed fibonacci sequence for: {nterms}")


async def main():
    task1 = asyncio.create_task(fibonacci(10000))
    task2 = asyncio.create_task(fibonacci(100000))
    task3 = asyncio.create_task(fibonacci(1000000))

    await task1, task2, task3

access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJyZWZyZXNoYWJsZSI6dHJ1ZSwic3ViIjoiMDA4OWFlODctNzVhZi00MWYwLTk2M2UtZTAwYzRhNGI5NjU1IiwiYXVkIjoiZ2V0YnV4LmNvbSIsInNjcCI6WyJhcHA6bG9naW4iLCJydGY6bG9naW4iLCJib3M6YXBwbGljYW50Il0sImV4cCI6MTkyMDMwODUyNywiaWF0IjoxNjA0OTQ4NTI3LCJqdGkiOiJkMWYwYTZhZS1jZDExLTRhMmYtYTRkNS04YzAwMzBkOTBhYTkiLCJjaWQiOiI4NDczNjIyOTQxIn0.ljKMDkPz7Fp7F1GroFv7irL0xPEB-23Pvsl41YtpzoU'


def test(e: SubscriberEvent):
    print(f'Event fired!: {e.event}')

def test2(e: SubscriberEvent):
    print(f'Event fired2!: {e.event}')


if __name__ == '__main__':
    subscriber = BUXSubscriber(access_token)
    subscriber.subscribe(test)
    subscriber.subscribe(test2)
    subscriber.start()
    #asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(subscriber.start())
