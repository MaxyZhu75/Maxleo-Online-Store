from re import S
import socket
import unittest
import requests
import warnings
import json
import os

# Set IP adresseses of frontend, catalog and order as environment variables
FRONT = os.getenv('FRONT', '107.21.136.71')
CATALOG = os.getenv('CATALOG', '107.21.136.71')
ORDER = os.getenv('ORDER', '107.21.136.71')
# API url path
frontend_query_url = 'http://%s:6060/products?toyname=' % FRONT
frontend_queryOrder_url = 'http://%s:6060/orders?ordernum=' % FRONT
frontend_buy_url = 'http://%s:6060/orders' % FRONT
catalog_query_url = 'http://%s:10086/query?toyname=' % CATALOG
catalog_buy_url = 'http://%s:10086/buy' % CATALOG
order_place_url = 'http://%s:10012/orders?toyname=' % ORDER
order_query_url = 'http://%s:10012/query?num=' % ORDER
order_heartbeat_url = 'http://%s:10012/heartbeat' % ORDER
order_notifyNewLeader_url = 'http://%s:10010/leaderis?leader=' % ORDER


# For different HTTP GET / HTTP POST, all the possible HTTP responses are described in design document Part 1 Section 2.1. And we created 13 test cases which correspond to 13 possible HTTP responses
# Notice that following test cases are effective only when database is in initial state, because expected response is configued statically in following codes!!! Of course, you can also design your own test case simply by configuring request parameters and expected responses in the method.
# For each test case, if our app & micro-services work correctly, by typing the command we provide, Python unittest will tell you ok on your terminal(all cases should be ok)!!!
class TestFunctionality(unittest.TestCase):

    def test_app_client_query_valid(self): # Testcase1: client sends valid HTTP GET to front-end server for querying product info
        r = requests.get(frontend_query_url + 'Tux')
        actual = r.json()
        expected = {'name': 'Tux', 'price': 25.99, 'quantity': 100}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_query_invalid(self): # Testcase2: client sends invalid HTTP GET to front-end server for querying product info
        r = requests.get(frontend_query_url + 'invalid')
        actual = r.json()
        expected = {"error": {"code": 404, "message": "product not found"}}
        #warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_frontend_catalog_valid(self): # Testcase3: front-end server sends valid HTTP GET to catalog server
        r = requests.get(catalog_query_url + 'Whale')
        actual = r.json()
        expected = {"data": {"name": "Whale", "price": 34.99, "quantity": 100}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_frontend_catalog_invalid(self): # Testcase4: front-end server sends invalid HTTP GET to catalog server
        r = requests.get(catalog_query_url + 'invalid')
        actual = r.json()
        expected = {"error": {"code": 404, "message": "product not found"}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_frontend_placeOrder_valid(self): # Testcase5: front-end server sends valid HTTP GET to order server
        r = requests.get(order_place_url + 'Clue&&quantity=15')
        actual = r.json()
        expected = {"order_number": 1}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_frontend_placeOrder_invalid(self): # Testcase6: front-end server sends invalid HTTP GET to order server
        r = requests.get(order_place_url + 'invalid&&quantity=15')
        actual = r.json()
        expected = {"order_number": -1, "message": "product not found"}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_frontend_placeOrder_outofstock(self): # Testcase7: front-end server sends valid HTTP GET to order server, but product is out of stock
        r = requests.get(order_place_url + 'Elephant&&quantity=100000')
        actual = r.json()
        expected = {"order_number": -1, "message": "out of stock"}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_buy_valid(self): # Testcase8: client sends valid HTTP POST to front-end server
        data = json.dumps({"toyname": "Pinball", "quantity": "10"})
        r = requests.post(url = frontend_buy_url, data = data)
        actual = r.json()
        expected  = {'order_number': 2}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_buy_invalid(self): # Testcase9: client sends invalid HTTP POST to front-end server
        data = json.dumps({"toyname": "invalid", "quantity": "10"})
        r = requests.post(url = frontend_buy_url, data = data)
        actual = r.json()
        expected = {'message': 'product not found', 'order_number': -1}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_buy_outofstock(self):# Testcase10: client sends valid HTTP POST to front-end server, but product is out of stock
        data = json.dumps({"toyname": "Bird", "quantity": "100000"})
        r = requests.post(url = frontend_buy_url, data = data)
        actual = r.json()
        expected = {'message': 'out of stock', 'order_number': -1}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        
    def test_microservices_order_cata_valid(self): # Testcase11: order server sends valid HTTP POST to catalog server
        data = json.dumps({"toyname": "Uno", "quantity": "5"})
        r = requests.post(url = catalog_buy_url, data = data)
        actual = r.json()
        expected = {'message': 'order has been placed'}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_order_cata_invalid(self): # Testcase12: order server sends invalid HTTP POST to catalog server
        data = json.dumps({"toyname": "invalid", "quantity": "5"})
        r = requests.post(url = catalog_buy_url, data = data)
        actual = r.json()
        expected = {'message': 'product not found'}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        
    def test_microservices_order_cata_outofstock(self): # Testcase13: order server sends valid HTTP POST to catalog server, but product is out of stock
        data = json.dumps({"toyname": "Risk", "quantity": "100000"})
        r = requests.post(url = catalog_buy_url, data = data)
        actual = r.json()
        expected = {'message': 'out of stock'}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
    
    def test_app_client_queryOrder_valid(self): # Testcase14: client sends valid HTTP GET to front-end server for querying order info
        r = requests.get(frontend_queryOrder_url + '1')
        actual = r.json()
        expected = {'data': {'number': 1, 'name': 'Clue', 'quantity': '15'}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_queryOrder_invalid(self): # Testcase15: client sends invalid HTTP GET to front-end server for querying order info
        r = requests.get(frontend_queryOrder_url + '10')
        actual = r.json()
        expected = {'error': {'code': 404, 'message': 'order not found'}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
    
    def test_microservices_frontend_queryOrder_valid(self): # Testcase16: front-end server sends valid HTTP GET to order server for querying order info
        r = requests.get(order_query_url + '2')
        actual = r.json()
        expected = {'data': {'number': 2, 'name': 'Pinball', 'quantity': '10'}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_frontend_queryOrder_invalid(self): # Testcase17: front-end server sends invalid HTTP GET to order server for querying order info
        r = requests.get(order_query_url + '10')
        actual = r.json()
        expected = {'error': {'message': 'order not found', 'code': 404}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        
    def test_microservices_frontend_heartbeat_valid(self): # Testcase18: front-end server sends heartbeat message to all the order servers in cluster for health check
        r = requests.get(order_heartbeat_url)
        actual = r.json()
        expected = {'idnum': 3}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
    
    def test_microservices_frontend_notifyNewLeader_valid(self): # Testcase19: front-end server sends notification to all the order servers in cluster when leader is changed
        r = requests.get(order_notifyNewLeader_url + '3')
        actual = r.json()
        expected = {'message': 'received'}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
