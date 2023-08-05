import websockets
import asyncio
import multiprocessing
import json
import time

class ShopifyStream(object):
    def __init__(self, websocket_url='wss://stream.ayinope.com'):
        self.product_queue = multiprocessing.Queue()
        self.websocket_url = websocket_url
        self.connection_process = multiprocessing.Process(target=self.__connection_wrapper).start()

    def __connection_wrapper(self):
        asyncio.get_event_loop().run_until_complete(self.connect(self.websocket_url))

    async def connect(self, websocket_url):
        async with websockets.connect(websocket_url) as websocket:
            while True:
                message = await websocket.recv()
                product = json.loads(message)
                self.product_queue.put(product)

    def wait_for_product(self, domain=None, include=None, exclude=None):
        while True:
            if not self.product_queue.empty():
                product = self.product_queue.get()
                to_return = product
                if domain and domain not in product['url']:
                    to_return = None
                if include and not all([x.lower() in product['title'].lower() for x in include]):
                    to_return = None
                if exclude and any([x.lower() in product['title'].lower() for x in exclude]):
                    to_return = None
                if to_return:
                    return to_return
            time.sleep(0.01)
