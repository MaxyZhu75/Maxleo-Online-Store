from threading import Thread, Condition
import threading
import socket



# Toy warehouse
products = {'Tux':{'price':25.99, 'stock': 5},   # Static parameters(price and stock) to be set
          'Whale':{'price':34.99, 'stock':0}}



# Handwritten queue class
class Myqueue(object):
    def __init__(self,) -> None:
        super().__init__()
        self.elements = []    # Array based queue
        self.len = 0          # Size of queue
        self.front = 0        # Head of queue
        
    def enqueue(self, item):       # Push items into queue
        self.elements.append(item)
        self.len += 1
    
    def dequeue(self):             # Pop items out of queue
        item = self.elements[0]
        self.len -= 1
        self.elements = self.elements[1:]
        return item
    
    def print(self):               # Check out the items
        print(self.elements)
        
    def isEmpty(self):             # Check out if the queue is empty
        if self.len == 0:
            return True
        return False
 


# Producer thread class
class ConnectionHandleThread(Thread):
    def run(self):
        
        global requestQueue
        global myserver
        
        while 1:

            conn,addr = myserver.accept()          # Producer accepts connections and receives requests
            print(addr, 'connected...')
            if condition.acquire():                # Check out if we can acquire the underlying lock
                requestQueue.enqueue((conn,addr))  # Once producer acquires the lock, it pushes request into the queue
                condition.notify()                 # Wake up other threads
                condition.release()                # Release the underlying lock
 


# Consumer thread class
class MessageHandleThread(Thread):
     def run(self):
        
        global requestQueue
        
        while 1:
            
            if condition.acquire():             # Check out if we can acquire the underlying lock
                if requestQueue.isEmpty():      # Check out if the request queue is empt
                    condition.wait()            # Release the lock, and blocks until it is awakened by a notify()
                else: 
                    t = threading.currentThread()
                    print('%s fetches a request from the queue!' %t.getName())
                    c,addr = requestQueue.dequeue() # Consumer fetches request from the queue
                    condition.notify()              # Wakes up other threads and starts executing
                    while 1:
                        data = c.recv(1024)
                        result=Query(data.decode('utf8'))
                        c.send(str(result).encode('utf-8')) # Request is processed and sent back by consumer
                        c.close()
                        break
                    print('Query has been done, %s is available!' %t.getName())

                condition.release()     # Release the underlying lock
                    


# Query method
# Parameter: toyName
# Return: price of toys
def Query(toyName):
    if toyName not in products:         # case1: item is not found in toy warehouse
        return -1
    if products[toyName]['stock'] == 0: # case2: item is out of stock 
        return 0
    return products[toyName]['price']   # case3: item is in stock



# Main
# Server starts up
requestQueue = Myqueue()
condition = Condition()

myserver = socket.socket()  # Regular socket connection at server
host = '0.0.0.0'
port = 10086                # Static parameter to be set
myserver.bind((host,port))
myserver.listen(5)
print('Server start successfully...')

ConnectionHandleThread().start()    # Run the producer thread at first
print('Thread-1 runs as producer...')

threadNum = int(input('Please configure the size of your thread pool:'))  # Set up your thread pool
for i in range(threadNum):
    MessageHandleThread().start()   # Run the consumer threads
    t = threading.currentThread() 
    threadName = 'Thread-%d' %(i+2) # Rename each theads here, and then we can see clear outputs when thread is working
    t.setName(threadName)
    print('Add %s' % t.getName())
print('Thread pool has been set up...')
