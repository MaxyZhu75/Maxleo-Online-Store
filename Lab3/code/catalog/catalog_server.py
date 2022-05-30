import json
import socket
import threading
from time import sleep
from flask import Flask, request
import requests

app = Flask(__name__)           # apply Flask web framework
database = []                   # chache
lock = threading.Lock()         # lock for memory databse
disk_lock = threading.Lock()    # lock for disk databse


# Notify front-end server for cache consistency
def notify_frontend_cach(name):
    requests.get('http://0.0.0.0:6060/rmcache?name=%s'%name)


# Check remaining quantity of every toy every 10 seconds, if a toy is out of stock the catalog service will restock it to 100
def check_quantity():
    while True:
        with lock:
            flag=False
            for item in database:
                if item['quantity']==0:
                    item['quantity']=100
                    notify_frontend_cach(item['name'])
                    flag=True
            if flag:
                writeInFile()
        sleep(10)
    

# Initialize the databse
def init_database():
    with open('database.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split(' ')
            item = {
                'name': info[0],
                'price': float(info[1]),
                'quantity': int(info[2])
            }
            database.append(item)
    f.close()


# Write operation
def writeInFile():
    global database
    data = ''
    for item in database:
        data += '%s %s %s\n' % (item['name'], item['price'], item['quantity'])
    # lock file in disk
    with disk_lock:
        f = open('database.txt', 'w')
        f.write(data)
        f.close()


# Query product info API
@app.route('/query', methods=['GET'])
def products():
    global database
    toyName = request.args.get('toyname')
    print(toyName)
    with lock:
        for item in database:
            if item['name'] == toyName:           # case1: HTTP GET JSON Response(successful Query)
                js = json.dumps({'data': item})
                return js
        js = json.dumps(                          # case2: HTTP GET JSON Response(unsuccessful Query)
            {'error': {
                'code': 404,
                'message': 'product not found'
            }})
        return js, 404


# Buy product API
@app.route('/buy', methods=['POST'])
def buy():
    data = request.data
    data = str(data, 'utf-8')
    data = eval(data)
    print(data)
    toyName, quantity = data['toyname'], data['quantity']
    print('name: %s, quantity: %s' % (toyName, quantity))
    with lock:
        for item in database:
            if item['name'] == toyName:
                if item['quantity'] - int(quantity) >= 0:
                    item['quantity'] -= int(quantity)
                    js = json.dumps({'message': 'order has been placed'}) # case1: HTTP POST JSON Response(successful Buy)
                    writeInFile()
                    # notify frontend
                    notify_frontend_cach(toyName)
                    return js
                else:
                    js = json.dumps({'message': 'out of stock'})          # case2: HTTP POST JSON Response(unsuccessful Buy)
                    return js, 404
        js = json.dumps({'message': 'product not found'})                 # case3: HTTP POST JSON Response(unsuccessful Buy)
        return js, 404


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    # host=get_ip()
    port=10086
    init_database()
    print(database)
    threading.Thread(target=check_quantity).start()
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
