import os
from random import randint, random
from time import time
import requests


# IP addresses of front-end server will be delivered as an environment variable because in Part 2 the server IP address might change
FRONT_HOST = os.getenv('FRONT', '10.0.0.240')
url = 'http://%s:6060/products/' % FRONT_HOST
p = os.getenv('p', 0.5)                             # Probability “p” will be delivered as an environment for Mode 1
p = float(p)
products = ['Tux', 'Whale', 'Elephant', 'Bird']

# Mode 1: Query and Buy randomly
def mode_case_1(s):
    r = s.get(url=url + products[randint(0, 3)])    # Send an HTTP GET to front-end server
    print(r.json())
    name, quantity = r.json()['name'], r.json()['quantity']
    if quantity > 0:                                # If the returned quantity is greater than 0, with probability “p” it will send an order request
        if random() <= p:
            num_buy = randint(1, 10)
            print('random buy %s, number %s' % (name, num_buy))
            resp = requests.post('http://%s:6060' % FRONT_HOST,    # Send an HTTP POST to front-end server
                                 data={
                                     'name': name,
                                     'quantity': num_buy
                                 })
            print(resp.text)


# Mode 2: Initiate a serials of Query
def mode_case_2(s):
    product = input('input the name of product:\n')
    num = int(input('input request times:\n'))
    start_time = time()
    for i in range(num):
        r = s.get(url + product)                           # Send a serials of HTTP GET to front-end server
        print(r.json())
    end_time = time()
    print('running time: ', end_time - start_time, 's')


# Mode 3: Initiate a serials of Buy
def mode_case_3(s):
    product = input('input the name of product: \n')
    quantity = int(input('input quantity\n'))
    num = int(input('input request times:\n'))
    start_time = time()
    for i in range(num):
        r = requests.post('http://%s:6060' % FRONT_HOST,    # Send a serials of HTTP POST to front-end server
                          data={
                              'name': product,
                              'quantity': quantity
                          })
        print(r.json())
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
