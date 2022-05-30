import json
import os
import socket
import threading
from flask import Flask, request
import requests
from shutil import copyfile

app = Flask(__name__)    # apply Flask web framework
lock = threading.Lock()  # lock for order log
order_cach = []          # chache
order_serves = ['10010', '10011', '10012']
leaderid = '-1'          # global variable saving leader ID


# Order number generator
class Counter:

    def __init__(self):
        self.value = self.init()
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1
            idNum = self.value
            return idNum

    def init(self):
        # if oder_log file exist
        if os.path.exists('order_log%s.txt' % id):
            with lock:
                f = open('order_log%s.txt' % id, 'r')
                lines = f.readlines()
                # find the latest non-negative order number
                for line in reversed(lines):
                    if int(line.split(' ')[0]) > 0:
                        return int(line.split(' ')[0])
                return 0
        else:
            return 0


# Qurey oder info API
@app.route('/query', methods=['GET'])
def query():
    num = request.args.get('num')
    for item in order_cach:
        if item['number'] == int(num):
            js = json.dumps({
                'data': {
                    'number': item['number'],
                    'name': item['name'],
                    'quantity': item['quantity']
                }
            })
            return js
    js = json.dumps({'error': {'code': 404, 'message': 'order not found'}})
    return js, 404


# Buy product API
@app.route('/orders', methods=['GET'])
def orders():
    toyName = request.args.get('toyname')
    quantity = request.args.get('quantity')
    data = json.dumps({'toyname': toyName, 'quantity': quantity})
    r = requests.post(url='http://0.0.0.0:10086/buy', data=data)
    if r.status_code == 200:
        idNum = idGenerator.increment()
        js = json.dumps({"order_number": idNum})
        with lock:
            order_cach.append({
                'number': idNum,
                'name': toyName,
                'quantity': quantity
            })
            f = open('order_log%s.txt' % id, 'a+')
            f.write("{orderId} {product} {quantity}\n".format(
                orderId=idNum, product=toyName, quantity=quantity))
            f.close()
        order_detail = json.dumps({
            'number': idNum,
            'name': toyName,
            'quantity': quantity
        })
        notify_others(order_detail)   # Once an order is placed successfully, notify other order nodes in the cluster
        return js
    elif r.status_code == 404:
        idNum = -1
        js = json.dumps({
            "order_number": idNum,
            'message': r.json()['message']
        })
        with lock:
            order_cach.append({
                'number': idNum,
                'name': toyName,
                'quantity': quantity
            })
            f = open('order_log%s.txt' % id, 'a+')
            f.write("{orderId} {product} {quantity}\n".format(
                orderId=idNum, product=toyName, quantity=quantity))
            f.close()
        order_detail = json.dumps({
            'number': idNum,
            'name': toyName,
            'quantity': quantity
        })
        notify_others(order_detail)   # Once an order is placed successfully, notify other order nodes in the cluster
        return js, 404
    else:
        return 'unexpected error%s' % r.status_code


# Order log consistency API for followers
@app.route('/notify', methods=['POST'])
def notify():
    data = request.data
    data = str(data, 'utf-8')
    data = eval(data)
    print(data)
    number, name, quantity = data['number'], data['name'], data['quantity']
    if number!=-1:
        idGenerator.increment()
    # Store in memory and write in log
    with lock:
        order_cach.append({
            'number': number,
            'name': name,
            'quantity': quantity
        })
        f = open('order_log%s.txt' % id, 'a+')
        f.write("{orderId} {product} {quantity}\n".format(orderId=number,
                                                          product=name,
                                                          quantity=quantity))
        f.close()
    return 'OK'
    

# Order log consistency API for leader
def notify_others(data):
    i = 1
    for order in order_serves:
        # no need to send request to itself
        if i != id:
            try:
                r = requests.post('http://0.0.0.0:%s/notify' % order,
                                  data=data)
            except Exception:
                print('%s failed!' % order)
        i += 1


# Receive leader id API
@app.route('/leaderis', methods=['GET'])
def leaderis():
    global leaderid
    leaderid = request.args.get('leader')
    return json.dumps({'message': 'received'})


# Heartbeat message API
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    js = json.dumps({"idnum": id})
    return js


# Initialize order log file
def init_order():
    if os.path.exists('order_log%s.txt' % id):
        with open('order_log%s.txt' % id, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                info = line.split(' ')
                item = {
                    'number': info[0],
                    'name': info[1],
                    'quantity': info[2]
                }
                order_cach.append(item)
        f.close()


def getport():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            infos = json.load(f)
            f.close()
        info = infos[-1]
        id, port = info['id'] + 1, info['port'] + 1
        infos.append({'id': id, 'port': port})
        with open('config.json', 'w') as f:
            json.dump(infos, f)
            f.close()
            return port, id
    else:
        with open('config.json', 'w') as f:
            data = []
            data.append({'id': 1, 'port': 10010})
            json.dump(data, f)
            f.close()
            return 10010, 1


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# Pull the latest order log from other nodes when restart 
def replica_log():
    if os.path.exists('order_log1.txt') or os.path.exists(
            'order_log2.txt') or os.path.exists('order_log3.txt'):
        if id == 1:
            copyfile('order_log2.txt', 'order_log1.txt')
        else:
            source_file = 'order_log%s.txt' % ((id - 1) % 3)
            dis_file = 'order_log%s.txt' % id
            copyfile(source_file, dis_file)


if __name__ == '__main__':
    id = int(os.getenv('ID', 5))
    port = os.getenv('PORT', 10010)
    replica_log()
    idGenerator = Counter()
    init_order()
    print(order_cach)
    print(port, ' ', id)
    app.run(host='0.0.0.0', port=port, threaded=True)
