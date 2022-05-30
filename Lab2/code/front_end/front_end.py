from concurrent.futures import ThreadPoolExecutor
import json
import socket
import threading
import requests
import os

response = """\
HTTP/1.1 {status_code} {status_message}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""

# IP addresses of catalog server and order server will be delivered as an environment variable because in Part 2 the server IP address might change
catalog_server_addr = os.getenv('CATALOG', 'catalog')
order_server_addr = os.getenv('ORDER', 'order')

print(order_server_addr)
print(type(order_server_addr))

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


# Process the HTTP GET request from client
def query(data, c):
    path = data.splitlines()[0].split(' ')[1]    # Obatain parameters from requests body
    func = path.split('/')[1]

    if func == 'products':                       # Filter invalid bad requests 
        product = path.split('/')[2]
        path = 'http://' + catalog_server_addr + ':10086/' + product
        print(path, flush=True)
        r = requests.get('http://' + catalog_server_addr + ':10086/' + product)   # Forward an HTTP GET to catalog server
        resp = r.json()
        if r.status_code == 200:                 # Check out the HTTP GET response from catalog server
            print(resp['data']['name'],
                  resp['data']['price'],
                  resp['data']['quantity'],
                  flush=True)
            payload = json.dumps({
                "name": resp['data']['name'],
                'price': resp['data']['price'],
                'quantity': resp['data']['quantity']
            })
            c.send(
                response.format(status_code=200,   # case1: HTTP GET JSON Response(successful Query)
                                status_message="OK",
                                content_length=len(payload),
                                payload=payload).encode("utf-8"))
        else:
            payload = json.dumps(resp)
            c.send(
                response.format(status_code=404,   # case2: HTTP GET JSON Response(unsuccessful Query)
                                status_message="ERROR",
                                content_length=len(payload),
                                payload=payload).encode("utf-8"))
    else:
        payload == json.dumps(
            {'error': {
                'code': 404,
                'message': 'product not found'
            }})
        c.send(
            response.format(status_code=404,       # Help filter invalid bad requests 
                            status_message="Not Found",
                            content_length=len(payload),
                            payload=payload).encode("utf-8"))


# Process the HTTP POST request from client
def order(data, c):
    try:
        toyName, quantity = data.splitlines()[-1].split('&')[0].split(    # Obatain parameters from requests body
        '=')[1], data.splitlines()[-1].split('&')[1].split('=')[1]
    except IndexError:
        print(data)
        return
    print('name: %s, quantity: %s' % (toyName, quantity), flush=True)
    url = 'http://%s:10010/%s/%s' % (order_server_addr, toyName, quantity)
    print(url, flush=True)
    r = requests.get(url)          # Forward an HTTP GET to order server

    if r.status_code == 200:       # Check out the HTTP GET response from order server
        payload = json.dumps({'data': {'order_num': r.json()['order_number']}})
        c.send(
            response.format(status_code=200,   # case1: HTTP GET JSON Response(successful Buy)
                            status_message="OK",
                            content_length=len(payload),
                            payload=payload).encode("utf-8"))
    else:
        payload = json.dumps(
            {'error': {
                'code': r.status_code,
                'message': r.json()['message']
            }})
        c.send(
            response.format(status_code=404,   # case2: HTTP GET JSON Response(unsuccessful Buy)
                            status_message="Not Found",
                            content_length=len(payload),
                            payload=payload).encode("utf-8"))


# Dispatch clients requests properly
# Front-end does NOT implement the Query or Buy. Rather it will forward the request to the other servers depending on request type
def request_handler(c, add):
    while True:
        try:
            data = c.recv(1024)
        except:
            break
        if not data:
            break
        data = data.decode('utf-8')

        if data.splitlines()[0].split(' ')[0] == 'GET':
            query(data, c)
        elif data.splitlines()[0].split(' ')[0] == 'POST':
            order(data, c)

    c.close()
    print('sesson closed', flush=True)


def main():
    HOST = get_ip()
    PORT = 6060
    s = socket.socket()  # Regular Socket programming
    s.bind((HOST, PORT))
    s.listen(1)
    print('front_end server running on: %s:%s' % (HOST, PORT), flush=True)
    # Server loop
    while True:
        c, add = s.accept()
        threading.Thread(target=request_handler, args=(c, add)).start()


main()
