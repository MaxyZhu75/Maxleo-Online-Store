# 📲 Team Members


**Maoqin Zhu**


* Implemented order server, automatted test source code. Test and help debug.


* Write design document, output document and evaluation ducument. Add inline comments in source codes.


**Yixiang Zhang**


* Implemented client, front-end server, catalog server, test source code.


* Test and help debug.


Thank you so much for your patience. If there is any configuration question, feel free to reach me out!


* Email: maoqinzhu@umass.edu or yixiangzhang@umass.edu



# 💻 Part 1 - Implement Your Multi-Tiered Toy Store as Microservices
![part1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/part1.jpg)


## Server Start Up Tutorial (on EdLab)
**Step1:** Log in the UMass EdLab remote server, and upload our source code files as follows.


![edlab1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/edlab1.png)


**Step2:** Use following command to start up servers in specific order as described in design document. Note that when starting a server, we will print its IP address on your screen. You should type that IP address as environment variable for the next one.


**$ python3 catalog_server.py**


**$ CATALOG=128.119.243.175 python3 order_server.py**


**$ CATALOG=128.119.243.175 ORDER=128.119.243.175 python3 front_end.py**


![edlab2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/edlab2.png)
![edlab3](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/edlab3.png)
![edlab4](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/edlab4.png)


## Functional Test Tutorial
Looking at **"test_func.py"**, for different HTTP GET / HTTP POST, we created 13 test cases which correspond to 13 possible HTTP responses described in [design document](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/design%20document.pdf) Part 1 Section 2.1.


**Notice that our test cases are effective only when database is in initial state, because expected response is configured statically in testing codes!!!** Of course, you can also run your own test case simply by configuring request parameters and expected responses in the method. The initial state of database should be:


![database1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/database1.png)



Looking at **“test_func.sh”**, this shell file will help us run all the 13 test cases.


**Notice that each time if you are running this shell, please configure those IP addresses(environment variables) manually. Thank you!!!** And also be careful when you do local test. When starting a server, we will print IP address on your screen. Type that IP address as environment variable rather than “127.0.0.1”.


![shell1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/shell1.png)


**Step1:** Type the following command:


**$ sh test_func.sh**


For each test case(valid/invalid requests), if our application or micro-services work correctly, Python unittest will tell “ok” on your terminal. As you can see, all the functionalities is working correctly as follows.



![func1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/func1.png)


And also, after finishing those 13 test cases, we can see the order log has been recorded correctly (**order ID is -1** if the order has not been placed), and the database has been persisted too.


![func2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/func2.png)
![func3](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/func3.png)



**Step2:** Looking at **“client.py”**, we implemented 3 modes for you. Type the following command:


**$ FRONT=128.119.243.175 p=0.5 python3 client.py**


**Mode 1:** Query and Buy randomly: It randomly queries an item, if the returned
quantity is greater than 0, with probability “p”(environment variable initialized in terminal) it will send an order request.


**Mode 2:** Initiate a serials of Query
You can specify the toy name and query times as you want. 


**Mode 3:** Initiate a serials of Buy
You can specify the toy name, quantity and number of requests as you want.


![client1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/client1.png)
![client2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/client2.png)



## Load Test Tutorial
Looking at **“test_load.py”**, it automatically sends **1000** HTTP GET/ **100** HTTP POST. Python unittest can help measure the total latency seen by clients in this case. Hence, in terms of average latency for each request, we should divide the total time by **1000** or by **100**. Here we vary the number of clients from 1 to 5 and measure the total latency as the load goes up. For each client terminal, type the following command as you want:


**$ FRONT=128.119.243.175 python3 -m unittest -v test_load.TestLoadPerformance.test_load_query**


**$ FRONT=128.119.243.175 python3 -m unittest -v test_load.TestLoadPerformance.test_load_load**


You could check out the [output document](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/output.pdf) for details, the testing result could be like:


![load1](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/load1.png)
![load2](https://github.com/umass-cs677/lab2-spring22-yixiang_l2/blob/main/docs/figures/part1/load2.png)



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

