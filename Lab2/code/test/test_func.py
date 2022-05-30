from re import S
import socket
import unittest
import requests
import warnings
import os

# Set IP adresseses of frontend, catalog and order as environment variables
FRONT = os.getenv('FRONT', '10.0.0.240')
CATALOG = os.getenv('CATALOG', '10.0.0.240')
ORDER = os.getenv('ORDER', '10.0.0.240')
frontend_query_url = 'http://%s:6060/products/' % FRONT
frontend_order_url = 'http://%s:6060/' % FRONT
catalog_url = 'http://%s:10086/' % CATALOG
order_url = 'http://%s:10010/' % ORDER


# HTTP communication between client and server / HTTP communication between between micro-services
def GET(s, url):
    r = s.get(url=url)
    return r.json()


def POST(url, port, toyName, quantity):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    s.send(
            b'POST /myself_login/ HTTP/1.1\r\nHost:172.19.0.4:8082\r\nContent-Type:application/x-www-form-urlencoded\r\nname=%s&quantity=%s'%(toyName,quantity)
        )
    r=s.recv(1024)
    r=r.split('\n')[-2]
    return r

# For different HTTP GET / HTTP POST, all the possible HTTP responses are described in design document Part 1 Section 2.1. And we created 13 test cases which correspond to 13 possible HTTP responses
# Notice that following test cases are effective only when database is in initial state, because expected response is configued statically in following codes!!! Of course, you can also design your own test case simply by configuring request parameters and expected responses in the method.
# For each test case, if our app & micro-services work correctly, by typing the command we provide, Python unittest will tell you ok on your terminal(all cases should be ok)!!!
class TestFunctionality(unittest.TestCase):

    def test_app_client_query_valid(self): # Testcase1: client sends valid HTTP GET to front-end server
        s = requests.Session()
        actual = GET(s, frontend_query_url + 'Tux')
        expected = {'name': 'Tux', 'price': 25.99, 'quantity': 80}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_app_client_query_invalid(self): # Testcase2: client sends invalid HTTP GET to front-end server
        s = requests.Session()
        actual = GET(s, frontend_query_url + 'invalid')
        expected = {"error": {"code": 404, "message": "product not found"}}
        #warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_microservices_frontend_catalog_valid(self): # Testcase3: front-end server sends valid HTTP GET to catalog server
        s = requests.Session()
        actual = GET(s, catalog_url + 'Tux')
        expected = {"data": {"name": "Tux", "price": 25.99, "quantity": 80}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_microservices_frontend_catalog_invalid(self): # Testcase4: front-end server sends invalid HTTP GET to catalog server
        s = requests.Session()
        actual = GET(s, catalog_url + 'invalid')
        expected = {"error": {"code": 404, "message": "product not found"}}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_microservices_frontend_order_valid(self): # Testcase5: front-end server sends valid HTTP GET to order server
        s = requests.Session()
        actual = GET(s, order_url + 'Whale/1')
        expected = {"order_number": 1}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_microservices_frontend_order_invalid(self): # Testcase6: front-end server sends invalid HTTP GET to order server
        s = requests.Session()
        actual = GET(s, order_url + 'invalid/1')
        expected = {"order_number": -1, "message": "product not found"}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_microservices_frontend_order_outofstock(self): # Testcase7: front-end server sends valid HTTP GET to order server, but product is out of stock
        s = requests.Session()
        actual = GET(s, order_url + 'Whale/10000000')
        expected = {"order_number": -1, "message": "out of stock"}
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        s.close()

    def test_app_client_buy_valid(self): # Testcase8: client sends valid HTTP POST to front-end server
        actual =POST(FRONT,6060,'Elephant','1')
        expected  = '{"data": {"order_num": 2}}'
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_buy_invalid(self): # Testcase9: client sends invalid HTTP POST to front-end server
        actual =POST(FRONT,6060,'invalid','1')
        expected = '{"error": {"code": 404, "message": "product not found"}}'
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_app_client_buy_outofstock(self):# Testcase10: client sends valid HTTP POST to front-end server, but product is out of stock
        actual =POST(FRONT,6060,'Elephant','100000')
        expected = '{"error": {"code": 404, "message": "out of stock"}}'
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        
    def test_microservices_order_cata_valid(self): # Testcase11: order server sends valid HTTP POST to catalog server
        actual =POST(CATALOG,10086,'Bird','1')
        expected = '{"message": "order has been placed"}'
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)

    def test_microservices_order_cata_invalid(self): # Testcase12: order server sends invalid HTTP POST to catalog server
        actual =POST(CATALOG,10086,'Invalid','1')
        expected = '{"message": "product not found"}'
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
        
    def test_microservices_order_cata_outofstock(self): # Testcase13: order server sends valid HTTP POST to catalog server, but product is out of stock
        actual =POST(CATALOG,10086,'Bird','100000')
        expected = '{"message": "out of stock"}'
        # warnings.simplefilter('ignore', ResourceWarning)
        self.assertEqual(actual, expected)
