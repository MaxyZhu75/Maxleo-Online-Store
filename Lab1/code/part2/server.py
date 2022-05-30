from concurrent.futures import ThreadPoolExecutor
from threading import Condition
import protobuf_pb2
import protobuf_pb2_grpc
import grpc



class ToyStoreServer(protobuf_pb2_grpc.ToyStoreServer):

    def __init__(self):
        self.data = initCataData()                                          # Initiate database

    def Query(self, request, context):
        toy = myQuery(self.data, request.name)                              # Server call local query method
        if toy is None:
            return protobuf_pb2.QueryResponse(stock=-1,price=-1)
        return protobuf_pb2.QueryResponse(stock=toy.stock,price=toy.price)  # Follow the message structure QueryResponse defined in proto file

    def Buy(self, request, context):
        result = myBuy(self.data, request.name)                             # Server call local query method
        return protobuf_pb2.BuyResponse(result=result)                      # Follow the message structure BuyResponse defined in proto file



# Implement buy method
def myBuy(data, toyname):
    condition.acquire()             # Try to acquire the underlying database lock
    for toy in data:
        if toy.name == toyname:     # Check out if the item bought by client exists in the databas
            if toy.stock == 0:      # Case 1: item is out of stock
                condition.release()
                return 0
            toy.stock -= 1          # Case 2: item is in stock
            condition.release()     
            return 1
    condition.release()             # Note that whatever the item bought by client is, we should always unlock database at the end
    return -1                       # Case 3: item is not in the database



# Implement query method
def myQuery(data, toyname):
    condition.acquire()          # Try to acquire the underlying database lock
    for toy in data:
        if toy.name == toyname:  # Check out if the query item exists in the database
            condition.release()  # Unlock the database
            return toy
    condition.release()
    return None



# Set up toy database
# Static parameters(price and stock) to be set
def initCataData():
    catagories = []
    toy_Tux = protobuf_pb2.Toy(name='Tux', stock=100, price=25.99)          # Follow the message structure Toy defined in proto file
    toy_Whale = protobuf_pb2.Toy(name='Whale', stock=100, price=34.99)
    toy_elephant = protobuf_pb2.Toy(name='Elephant', stock=100, price=29.99)
    toy_bird = protobuf_pb2.Toy(name='Bird', stock=50, price=39.99)
    catagories.append(toy_Whale)
    catagories.append(toy_Tux)
    catagories.append(toy_elephant)
    catagories.append(toy_bird)
    return catagories



 # Set up a server with which RPCs can be serviced
def server(maxNum):
    server = grpc.server(ThreadPoolExecutor(max_workers=maxNum))
    print('Thread pool has been set up...')
    protobuf_pb2_grpc.add_ToyStoreServerServicer_to_server(
        ToyStoreServer(), server)
    server.add_insecure_port('[::]:10086')  # Bind IP address and port number
    server.start()                          # Start your server
    print('Server start successfully..')
    server.wait_for_termination()           # Block the calling thread until the server terminates


# Main
# Server starts up
condition = Condition()
data = initCataData()
maxNum = input('Please type in the maximum number of threads:')
server(maxNum=int(maxNum))
