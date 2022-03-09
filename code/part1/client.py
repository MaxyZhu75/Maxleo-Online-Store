import socket
import time

para = input('Please type the toy name:') # Type the toy name parameter
requestNum= int(input('Specify how many requests you wanna send (type -1 if you do not wanna stop sending):')) # Select your mode. Note that if you do not wanna stop sending, input -1

if requestNum==-1:
    # Client request loop
    while 1:
        c = socket.socket()            # Regular socket connection at client machine
        host = 'elnux7.cs.umass.edu'   # Static parameters(IP address and port) to be set
        port = 10086
        c.connect((host, port))
        start_time = time.time()       # Start timer before RPC is made
        toyName = para
        c.send(toyName.encode('utf-8'))
        result = c.recv(1024)
        finish_time = time.time()      # Stop timer after response is revceived
        print('Query:', toyName)
        print('From Server:', result.decode())
        print('Latency:', finish_time-start_time, 's')  # Print current RPC information

else:
    for i in range(requestNum):
        c = socket.socket()            # Regular socket connection at client machine
        host = 'elnux7.cs.umass.edu'   # Static parameters(IP address and port) to be set
        port = 10086
        c.connect((host, port))
        start_time = time.time()       # Start timer before RPC is made
        toyName = para
        c.send(toyName.encode('utf8'))
        result = c.recv(1024)
        finish_time = time.time()      # Stop timer after response is revceived
        print('Query:', toyName)
        print('From Server:', result.decode())
        print('Latency:', finish_time-start_time, 's')  # Print current RPC information

