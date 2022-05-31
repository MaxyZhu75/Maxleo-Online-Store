# :elephant: Maxleo Online Store - Lab 2



You will see two programming parts in the following sections. In the first part, we aim to design distributed server applications using a multi-tier architecture and microservices. In the second part, we will learn how to use Docker to containerize our micro-service, and learn to manage an application consisting of multiple containers using Docker Compose.



# Part 1 - Implementation with Socket Connection and Handwritten Thread Pool



![part1](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/figures/part1/part1.jpg)



## Problem Statement



In this part, we implemented an online Toy store as a socket-based client-server application. Our design should be able multiple client processes making **concurrent requests to the server.** The main part of the assignment is to **implement our own ThreadPool** (not allowed to use a ThreadPool framework that are available by the language/libraries).



The server component should implement a single method Query, which takes a single string argument that specifies the name of the toy. The Query method returns the dollar price of the item (as a floating point value such as 25.99) if the item is in stock. It returns -1 if the item is not found and 0 if the item is found but not in stock. The client component should connect to the server using a socket connection. It should construct a message in the form of a buffer specifying the method name (e.g., string "Query") and arguments ("toyName"). The message is sent to the server over the socket connection. The return value is another buffer containing the cost of the item or an error code such as -1 and 0, as noted above.



# 💻 Part 2 - Containerize Your Application
![part2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/part2.jpg)


## Server Start Up Tutorial (on Local Machine)
**Step1:** Before running containers, we should build the Docker images.

**$ sudo docker build -f catalog_dockerfile . -t catalog**


**$ sudo docker build -f order_dockerfile . -t order**


**$ sudo docker build -f front_end_dockerfile . -t front_end**


![build1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/build1.png)


**Step2:** Then we can run dockers using Docker compose as follows.


**$ cd src**


**$ sudo docker-compose up**


![docker1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/docker1.png)


## Functional Test Tutorial
Looking at **"test_func.py"**, for different HTTP GET / HTTP POST, we created 13 test cases which correspond to 13 possible HTTP responses described in [design document](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/design%20document.pdf) Part 1 Section 2.1.


**Notice that our test cases are effective only when database is in initial state, because expected response is configured statically in testing codes!!!** Of course, you can also run your own test case simply by configuring request parameters and expected responses in the method. The initial state of database should be:


![database1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/database1.png)



Looking at **“test_func.sh”**, this shell file will help us run all the 13 test cases.


**Notice that each time if you are running this shell, please configure those IP addresses(environment variables) manually. Thank you!!!** And also be careful when you do local test. When starting a server, we will print IP address on your screen. Type that IP address as environment variable rather than “127.0.0.1”.


![shell1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/shell1.png)


**Step1:** Type the following command:


**$ sh test_func.sh**


For each test case(valid/invalid requests), if our application or micro-services work correctly, Python unittest will tell “ok” on your terminal. As you can see, all the functionalities is working correctly as follows.


![func1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/func1.png)
![func2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/func2.png)


And also, after finishing those 13 test cases, we can see the order log has been recorded correctly (**order ID is -1** if the order has not been placed), and the database has been persisted too.


![func3](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/func3.png)
![func4](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/func4.png)



**Step2:** Looking at **“client.py”**, we implemented 3 modes for you. Type the following command:


**$ FRONT=172.20.0.4 p=0.5 python3 client.py**


**Mode 1:** Query and Buy randomly: It randomly queries an item, if the returned
quantity is greater than 0, with probability “p”(environment variable initialized in terminal) it will send an order request.


**Mode 2:** Initiate a serials of Query
You can specify the toy name and query times as you want. 


**Mode 3:** Initiate a serials of Buy
You can specify the toy name, quantity and number of requests as you want.


![client1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/client1.png)


## Load Test Tutorial
Looking at **“test_load.py”**, it automatically sends **1000** HTTP GET/ **100** HTTP POST. Python unittest can help measure the total latency seen by clients in this case. Hence, in terms of average latency for each request, we should divide the total time by **1000** or by **100**. Here we vary the number of clients from 1 to 5 and measure the total latency as the load goes up. For each client terminal, type the following command as you want:


**$ FRONT=172.19.0.4 python3 -m unittest -v test_load.TestLoadPerformance.test_load_query**


**$ FRONT=172.19.0.4 python3 -m unittest -v test_load.TestLoadPerformance.test_load_buy**


You could check out the [output document](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/output.pdf) for details, the testing result could be like:


![load1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/loas1.png)
![load2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part2/load3.png)


## Way to Approach
Please check [design document](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/design%20document.pdf) for details.


## Simulation Results
Please check [Output](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/output.pdf) for details.

