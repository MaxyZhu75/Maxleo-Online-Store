import json
import socket
from time import sleep
import unittest
import requests
import warnings
import os

FRONT = os.getenv('FRONT', '107.21.136.71')
frontend_query_url = 'http://%s:6060/products?toyname=' % FRONT
frontend_queryOrder_url = 'http://%s:6060/orders?ordernum=' % FRONT
frontend_buy_url = 'http://%s:6060/orders' % FRONT


# Open multiple client terminals. By typing the command we provide at each console, Python unittest will tell you the latency on your terminal!!!
# Note: if you confroont a wrning, you could turn to warnings.simplefilter('ignore', ResourceWarning) as follows
class TestLoadPerformance(unittest.TestCase):

    def test_load_query(self):
        #warnings.simplefilter('ignore', ResourceWarning)
        for i in range(1000):
            response = requests.get(frontend_query_url + 'Jenga')

    def test_load_buy(self):
        #warnings.simplefilter('ignore',ResourceWarning)
        data = json.dumps({"toyname": "Sand", "quantity": "1"})
        for i in range(1000):
            response = requests.post(url = frontend_buy_url, data = data)
            
    def test_load_queryOrder(self):
        #warnings.simplefilter('ignore', ResourceWarning)
        for i in range(1000):
            response = requests.get(frontend_queryOrder_url + '1')
