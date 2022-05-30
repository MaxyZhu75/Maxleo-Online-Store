import socket
from time import sleep
import unittest
import requests
import warnings
import os

FRONT_HOST = os.getenv('FRONT', '10.0.0.240')
url = 'http://%s:6060/products/' % FRONT_HOST


def Query(s, toyName):
    r = s.get(url=url + toyName)                        # Send an HTTP GET to front-end server
    return r.json()


def Buy(toyName, quantity):
    formdata = {'name': toyName, 'quantity': quantity}
    r = requests.post('http://%s:6060' % FRONT_HOST,    # Send an HTTP POST to front-end server
                      data=formdata,
                      headers=headers)
    return r.json()


headers = {'Content-type': 'application/x-www-form-urlencoded'}

# Open multiple client terminals. By typing the command we provide at each console, Python unittest will tell you the latency on your terminal!!!
# Note: if you confroont a wrning, you could turn to warnings.simplefilter('ignore', ResourceWarning) as follows
class TestLoadPerformance(unittest.TestCase):

    def test_load_query(self):
        s = requests.Session()
        #warnings.simplefilter('ignore', ResourceWarning)
        for i in range(1000):
            Query(s, 'Whale')

    def test_load_buy(self):
        #warnings.simplefilter('ignore',ResourceWarning)
        for i in range(100):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((FRONT_HOST, 6060))
            s.send(
                b'POST /myself_login/ HTTP/1.1\r\nHost:128.119.243.168:8082\r\nContent-Type:application/x-www-form-urlencoded\r\nname=Whale&quantity=1'
            )
        
