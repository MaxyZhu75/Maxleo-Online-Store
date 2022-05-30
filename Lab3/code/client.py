import json
import os
from random import randint, random
from time import time
import requests

# IP addresses of front-end server will be delivered as an environment variable
FRONT_HOST = os.getenv('FRONT', '10.0.0.240')
url = 'http://%s:6060/products?toyname=' % FRONT_HOST
p = os.getenv(
    'p', 0.5)  # Probability “p” will be delivered as an environment for Mode 1
p = float(p)
products = [
    'Tux', 'Whale', 'Elephant', 'Bird', 'Risk', 'Sand', 'Jenga', 'Uno',
    'Pinball', 'Clue'
]


# Mode 1: Query and Buy randomly
def mode_case_1(s):
    start_time = time()
    r = requests.get(
        url=url +
        products[randint(0, 9)])  # Send an HTTP GET to front-end server
    end_time = time()
    print('query running time: ', end_time - start_time, 's')
    print(r.json())
    name, quantity = r.json()['name'], r.json()['quantity']
    if quantity > 0:              # If the returned quantity is greater than 0, with probability “p” it will send an order request
        if random() <= p:
            num_buy = randint(1, 10)
            print('random buy %s, number %s' % (name, num_buy))
            data = json.dumps({'toyname': name, 'quantity': num_buy})
            start_time = time()
            resp = requests.post(
                'http://%s:6060/orders' %
                FRONT_HOST,       # Send an HTTP POST to front-end server
                data=data)
            end_time = time()
            print('buy item running time: ', end_time - start_time, 's')
            print(resp.json())


# Mode 2: Initiate a serials of Query
def mode_case_2(s):
    product = input('input the name of product:\n')
    num = int(input('input request times:\n'))
    start_time = time()
    for i in range(num):
        r = requests.get(
            url + product)  # Send a serials of HTTP GET to front-end server
        print(r.json())
    end_time = time()
    print('running time: ', end_time - start_time, 's')


# Mode 3: Initiate a serials of Buy
def mode_case_3(s):
    product = input('input the name of product: \n')
    quantity = int(input('input quantity\n'))
    num = int(input('input request times:\n'))
    data = json.dumps({'toyname': product, 'quantity': quantity})
    start_time = time()
    for i in range(num):
        resp = requests.post(
                'http://%s:6060/orders' %
                FRONT_HOST,  # Send an HTTP POST to front-end server
                data=data)
        print(resp.json())
    end_time = time()
    print('running time: ', end_time - start_time, 's')


# Main
def get():
    s = requests.Session()
    while 1:
        msg = input('mode: \n')
        if str(msg) == '1':
            mode_case_1(s)
        elif str(msg) == '2':
            mode_case_2(s)
        elif str(msg) == '3':
            mode_case_3(s)
        elif str(msg) == '4':
            s.close()
        else:
            print('wrong code')


get()
