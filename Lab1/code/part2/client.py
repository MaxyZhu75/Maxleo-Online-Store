from concurrent.futures import thread
from logging import exception
from threading import Thread
from time import perf_counter, perf_counter_ns, time
import grpc
import protobuf_pb2
import protobuf_pb2_grpc



# Query method
def query(requestMsg):
    with grpc.insecure_channel('elnux7.cs.umass.edu:10086') as channel: # Create an insecure channel to a server
        stub = protobuf_pb2_grpc.ToyStoreServerStub(channel)            # gRPC client stub
        start_time = time()                                             # Start timer before RPC is made
        response = stub.Query(protobuf_pb2.RequestBody(name=requestMsg))
        end_time = time()                                               # Stop timer after response is revceived
        print('Query:', requestMsg)
        print('Price: %s,  Stock: %s' %(round(response.price, 4), response.stock))
        print('Latency:', end_time-start_time, 's')                     # Print current RPC information



# Buy method
def buy(requestMsg):
    with grpc.insecure_channel('elnux7.cs.umass.edu:10086') as channel: # Create an insecure channel to a server
        stub = protobuf_pb2_grpc.ToyStoreServerStub(channel)            # gRPC client stub
        start_time = time()                                             # Start timer before RPC is made
        response = stub.Buy(protobuf_pb2.RequestBody(name=requestMsg))
        end_time = time()                                               # Stop timer after response is revceived
        if response.result == -1:                                       # Case 1: item is not in the warehouse
            print('From Server: -1')
            print('Latency:', end_time-start_time, 's')
            raise Exception('Oops, invalid input. We do not have this product...')  # Exception processing
        elif response.result == 0:                                      # Case 2: item is out of stock
            print('From Server: 0')
            print('Latency:', end_time-start_time, 's')
            raise Exception('Sorry, this toy is out of stock...')       # Exception processing
        else:                                                           # Case 3: item is in stock
            print('From Server: 1')
            print('Your order has been placed successfully!!!')
            print('Latency:', end_time-start_time, 's')



# Main
# Client initialize
i = 0
requeMsg = input('Please type in toy name: ')                  # Type the toy name parameter
requestFunc = input('Please type in method(query or buy): ')   # Type the method name parameter
requestNum= int(input('Specify how many requests you wanna send (type -1 if you do not wanna stop sending):')) # Select your mode. Note that if you do not wanna stop sending, input -1

if requestNum == -1:                       # Mode 1: While true loop and keep sending requests
    while 1:
        i += 1
        print('---------------------')
        try:                               # Try-except for appropriate error/exception handling
            if requestFunc == 'query':
                query(requestMsg=requeMsg)
            elif requestFunc == 'buy':
                buy(requestMsg=requeMsg)
        except Exception as e:
            print('What we catch:', repr(e))
            break
else:                                      # Mode 2: For loop, send a certain number of requests as you configure
    for i in range(requestNum):
        print('---------------------')
        try:                               # Try-except for appropriate error/exception handling
            if requestFunc == 'query':
                query(requestMsg=requeMsg)
            elif requestFunc == 'buy':
                buy(requestMsg=requeMsg)
        except Exception as e:
            print('What we catch:', repr(e))
            break
