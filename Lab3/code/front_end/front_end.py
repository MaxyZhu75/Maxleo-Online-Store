import json
import os
import socket
import threading
from time import sleep
from flask import Flask, request
import requests

app = Flask(__name__)    # apply Flask web framework
products_cach = []       # chache
lock = threading.Lock()  # lock for memory

catalog_server_addr = os.getenv('CATALOG', 'catalog')
leader_server_addr = os.getenv('ORDER', 'order')
use_cach_flag = True     # caching switch for turning on/off


# Checkout cache
def isInCach(name):
    for item in products_cach:
        if item['name'] == name:
            return True
    return False


# Append to cache
def addCach(item):
    with lock:
        item = json.loads(item)
        products_cach.append(item)


# Remove from cache
def rmCache(name):
    if isInCach(name):
        with lock:
            i = 0
            for item in products_cach:
                if item['name'] == name:
                    products_cach.pop(i)
                    return 'OK'
                i += 1


# API for cache consistency
@app.route('/rmcache', methods=['GET'])
def rm():
    name = request.args.get('name')
    rmCache(name)
    return 'ok'


# Query product info API
@app.route('/products', methods=['GET'])
def products():
    toyName = request.args.get('toyname')
    print(toyName)
    if isInCach(toyName) and use_cach_flag: # Handle by cache
        for item in products_cach:
            if item['name'] == toyName:
                js = json.dumps(item)
                print('from cache')
                return js
    else:
        try:
            r = requests.get('http://0.0.0.0:10086/query?toyname=%s' % toyName) # Forward an HTTP GET to catalog server
            resp = r.json()
            if r.status_code == 200:        # case1: HTTP GET JSON Response(successful Query)
                print(resp['data']['name'],
                    resp['data']['price'],
                    resp['data']['quantity'],
                    flush=True)
                js = json.dumps({
                    "name": resp['data']['name'],
                    'price': resp['data']['price'],
                    'quantity': resp['data']['quantity']
                })
                addCach(js)
                return js
            elif r.status_code == 404:     # case2: HTTP GET JSON Response(unsuccessful Query)
                js = json.dumps(resp)
                return js, 404
            else:
                return 'unexpected error'
        except:
            return 'error'


# Return leader ID API
@app.route('/leader',methods=['GET'])
def leader():
    return json.dumps({'leader':leader_server_addr})


# Order API
@app.route('/orders', methods=['POST', 'GET'])
def orders():
    if request.method == 'GET':       # case1: query order info
        orderNum = request.args.get('ordernum')
        print(orderNum)
        r = requests.get('http://0.0.0.0:%s/query?num=%s' % (leader_server_addr,orderNum))
        if r.status_code == 200: 
            return r.json()
        elif r.status_code == 404: 
            return r.json()
        else:
            return 'unexpected error'
    elif request.method == 'POST':    # case2: buy product
        data = request.data
        data = str(data, 'utf-8')
        data = eval(data)
        print(data)
        toyName, quantity = data['toyname'], data['quantity']
        r = requests.get(
            'http://0.0.0.0:%s/orders?toyname=%s&&quantity=%s' %
            (leader_server_addr,toyName, quantity))
        return r.json()


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# Send heartbeat message for health check
def heartbeat():
    while True:
        try:
            requests.get('http://0.0.0.0:%s/heartbeat'%leader_server_addr)
        except Exception as e:
            leader_election()
        sleep(5)
    
    
# Implement leader election algorithm
def leader_election():
    order_servers=['10012','10011','10010']
    servers=[]
    for order in order_servers:
        try:
            r=requests.get('http://0.0.0.0:%s/heartbeat'%order)
            servers.append({'id':r.json()['idnum'],'port':order})
        except Exception as e:
            print('%s failed!'%order)
    servers=sorted(servers,key=lambda e:e.get('id',-1)) # Sort the order servers by ID
    global leader_server_addr
    leader_server_addr=servers[-1]['port']
    for order in order_servers:
        try:
            r=requests.get('http://0.0.0.0:%s/leaderis?leader=%s'%(order,leader_server_addr)) # Notify all the nodes in the cluster that a new leader is selected
        except Exception as e:
            print('%s failed!'%order)


if __name__ == '__main__':
    port=6060
    leader_election()
    print('now leader is %s'%leader_server_addr)
    threading.Thread(target=heartbeat).start()
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
