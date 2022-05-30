import socket
import json
import threading

response = """\
HTTP/1.1 {status_code} {status_message}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}
{payload}
"""
database = []                 # Maintain data in memory

lock = threading.Lock()       # lock for memory databse
disk_lock = threading.Lock()  # lock for disk databse


# Pass the server IP as an environment variable because in Part 2 the server IP address might change
# Note: when starting a server, we will print its IP address on your screen
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# Persist data on disk
def writeInFile():
    global database
    data = ''
    for item in database:
        data += '%s %s %s\n' % (item['name'], item['price'], item['quantity'])
    with disk_lock:   # Try to acquire the lock
        f = open('database.txt', 'w')
        f.write(data)
        f.close()


# Process the HTTP POST request from order server
def write(request, c):
    global database
    toyName, quantity = request.splitlines()[-1].split('&')[0].split(    # Obatain parameters from requests body
        '=')[1], request.splitlines()[-1].split('&')[1].split('=')[1]
    print('name: %s, quantity: %s' % (toyName, quantity), flush=True)

    with lock:                                  # Try to acquire the lock
        for item in database:
            if item['name'] == toyName:         # Validate the request and check out if the toy is in stock
                if item['quantity'] - int(quantity) >= 0:
                    item['quantity'] -= int(quantity)
                    js = json.dumps({'message': 'order has been placed'})
                    c.send(
                        response.format(status_code=200,   # case1: HTTP POST JSON Response(successful Buy)
                                        status_message="OK",
                                        content_length=len(js),
                                        payload=js).encode("utf-8"))
                    c.close()
                    writeInFile() # In terms of the persistent strategy, we write the data into disk every time we modify the data in memory
                    return
                else:
                    js = json.dumps({'message': 'out of stock'})
                    c.send(
                        response.format(status_code=404,   # case2: HTTP POST JSON Response(unsuccessful Buy)
                                        status_message="ERROR",
                                        content_length=len(js),
                                        payload=js).encode("utf-8"))
                    c.close()
                    return
        js = json.dumps({'message': 'product not found'})
        c.send(
            response.format(status_code=404,               # case3: HTTP POST JSON Response(unsuccessful Buy)
                            status_message="ERROR",
                            content_length=len(js),
                            payload=js).encode("utf-8"))
        c.close()
        return


# Process the HTTP GET request from front-end server
def read(request, c):
    global database
    toyName = request.splitlines()[0].split('/')[1].split(' ')[0]    # Obatain parameters from requests body
    print(toyName, flush=True)
    with lock:                                  # Try to acquire the lock
        for item in database:
            if item['name'] == toyName:         # Validate the request and check out if the toy is in stock
                js = json.dumps({'data': item})
                c.send(
                    response.format(status_code=200,   # case1: HTTP GET JSON Response(successful Query)
                                    status_message="OK",
                                    content_length=len(js),
                                    payload=js).encode("utf-8"))
                c.close()
                return
        js = json.dumps(
            {'error': {
                'code': 404,
                'message': 'product not found'
            }})
        c.send(
            response.format(status_code=404,           # case2: HTTP GET JSON Response(unsuccessful Query)
                            status_message="ERR",
                            content_length=len(js),
                            payload=js).encode("utf-8"))
        c.close()
        return


# Maintain data in memory for a speed up
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


# Handle the requests
def MsgHandler(c):
    request = c.recv(1024)
    request = request.decode("utf-8")
    if request.splitlines()[0].split(' ')[0] == 'GET':  # Process the HTTP GET request from front-end server
        read(request, c)
        print(request, flush=True)
    else:                                               # Process the HTTP POST request from order server
        write(request, c)
        print(request, flush=True)


def main():
    host = get_ip()
    port = 10086          # Reserve a port for your service
    s = socket.socket()
    s.bind((host, port))  # Bind to the port
    s.listen(5)           # Now wait for client connection
    print('catalog server running on: %s:%s' % (host, port), flush=True)
    init_database()
    print(database, flush=True)
    # Server loop
    while True:
        c, addr = s.accept()  # Establish connection with client
        print("Connected to :", addr[0], ":", addr[1],
              flush=True)     # Lock acquired by client
        t = threading.Thread(
            target=MsgHandler,
            args=(c, ))       # Start a new thread and return its identifier
        t.start()


main()
