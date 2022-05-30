from mimetypes import init
import os
import requests
import socket
import json
import threading

response = """\
HTTP/1.1 {status_code} {status_message}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""

lock = threading.Lock()

# IP addresses of catalog server will be delivered as an environment variable because in Part 2 the server IP address might change
catalog_server_addr = os.getenv('CATALOG', 'catalog')

print(catalog_server_addr)
print(type(catalog_server_addr))


# Ping DNS to obtain the IP address
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# Order number generator class which guarantees the ID is unique, incremental and starting from 0
# Note that: if an order is not placed successfully, order log will still record that with ID = -1
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
        if os.path.exists('order_log.txt'):
            with lock:
                f=open('order_log.txt','r')
                lines=f.readlines()
                for line in reversed(lines):      # Find the latest non-negative order number
                    if int(line.split(' ')[0])>0:
                        return int(line.split(' ')[0])
                return 0
        else:
            return 0
                        


idGenerator = Counter()



# Process the HTTP GET request from front-end server
def Buy(c):
    global idGenerator
    request = c.recv(1024)
    request = request.decode("utf-8")
    para = request.splitlines()[0].split('/')        # Obatain parameters from requests body
    toyName = para[1]
    toyQuantity = para[2].split(' ')[0]

    url = 'http://' + catalog_server_addr + ':10086'
    print(url, flush=True)
    r = requests.post(url, data={"toyName": toyName, "quantity": toyQuantity})    # Forward an HTTP POST to catalog server
    if r.status_code == 200:                         # Check out the HTTP GET response from catalog server
        idNum = idGenerator.increment()              # Generate an order number using our generator
        js = json.dumps({"order_number": idNum})
        c.send(
            response.format(status_code=200,         # case1: HTTP POST JSON Response(successful Buy)
                            status_message="Order has been placed",
                            content_length=len(js),
                            payload=js).encode("utf-8"))
    else:
        idNum = -1                                   # If an order is not placed successfully, order log will still record that with ID = -1
        js = json.dumps({
            "order_number": idNum,
            'message': r.json()['message']
        })
        c.send(
            response.format(status_code=404,         # case2: HTTP POST JSON Response(unsuccessful Buy)
                            status_message="Fail to buy",
                            content_length=len(js),
                            payload=js).encode("utf-8"))
    with lock:
        f = open('order_log.txt', 'a+')              # Maintain the order log
        f.write("{orderId} {product} {quantity}\n".format(
            orderId=idNum, product=toyName, quantity=toyQuantity))
        f.close()
    c.close()


def main():
    host = get_ip()
    port = 10010
    s = socket.socket()  # Regular Socket programming
    s.bind((host, port))
    s.listen(5)
    print('order server running on: %s:%s' % (host, port), flush=True)
    # Server loop
    while True:
        c, addr = s.accept()
        print("Connected to :", addr[0], ":", addr[1],
              flush=True)
        t = threading.Thread(
            target=Buy,
            args=(c, ))
        t.start()


main()
