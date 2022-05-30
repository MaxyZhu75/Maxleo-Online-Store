# 📲 Team Members


**Maoqin Zhu**


* Designed the application. Implemented automatted test source code. Test and help debug.


* Write design document, output document and evaluation ducument. Add inline comments in source codes.


**Yixiang Zhang**


* Designed the application. Implemented front-end server, catalog server, order server source code.


* Test and help debug.


Thank you so much for your patience. If there is any configuration question, feel free to reach me out!


* Email: maoqinzhu@umass.edu or yixiangzhang@umass.edu



# 💻 Lab 3: Caching, Replication and Fault Tolerance
![overview](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/Overview.png)


## Deployment Tutorial (on AWS)
**Step1:** First, start our EC2 instance as described in homework6.


**Step2:** Open specific ports on our EC2 instance. There are some ports to be opened in our lab: 22, 6060, 10086, 10010-10012


**$ aws ec2 authorize-security-group-ingress --group-name default --protocol tcp --port <number> --cidr 0.0.0.0/0**


![port](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/port.png)


**Step3:** Acess our EC2 instance and upload source code via SSH


![aws1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/aws1.png)
    

**Step4:** Start our application


We recommend you run following commands on our EC2 instance at first:
    
    
**$ sudo apt-get update**

    
**$ sudo apt-get -y install python3-pip**


**$ pip3 install flask**


Now in order to start our application, simply open 5 terminals on our AWS EC2 instance, and run micro services in each terminal in specific order. After cd into different directories, type the following commands.
    

**$ python3 catalog_server.py**

    
**$ ID=1 PORT=10010 python3 order_server.py**


**$ ID=2 PORT=10011 python3 order_server.py**

    
**$ ID=3 PORT=10012 python3 order_server.py**


**$ python3 front_end.py**

    
![aws2](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/aws2.png)

    
## Functional Test Tutorial
Looking at “test_func.py”, for different HTTP GET / HTTP POST, we created 19 test cases which correspond to 19 possible HTTP responses.
Notice that our test cases are effective only when database is in initial state, because expected response is configured statically in testing codes. Of course, you can also run your own test case simply by configuring request parameters and expected responses in the method.


**Notice that our test cases are effective only when database is in initial state, because expected response is configured statically in testing codes!!!** Of course, you can also run your own test case simply by configuring request parameters and expected responses in the method. The initial state of database should be:


![database1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/database.png)



Looking at **“test_func.sh”**, this shell file will help us run all the 13 test cases.


**Notice that each time if you are running this shell, please configure those IP addresses(environment variables) manually. Thank you!!!** And also be careful when you do local test. When starting a server, we will print IP address on your screen. Type that IP address as environment variable rather than “127.0.0.1”.


![shell1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/shell.png)


Type the following command:


**$ sh test_func.sh**


For each test case(valid/invalid requests), if our application or micro-services work correctly, Python unittest will tell “ok” on your terminal. As you can see, all the functionalities is working correctly as follows.


![func1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/func.png)


And also, after finishing those 19 test cases, we can see the database at catalog server has been recorded and persisted correctly.


![func2](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/func1.png)



## Load Test Tutorial
Looking at “test_load.py”, it automatically sends 1000 Query, Buy or queryOrder requests. Python unittest can help measure the total latency seen by clients in this case. Hence, in terms of average latency for each request, we should divide the total time by 1000. 
   
    
For different type of requests, we repeatedly run 5 clients at the same time, and measure the total latency seen by each client. There are 3 commands for each performance testing.


**$ FRONT=IP address python3 -m unittest -v test_load.TestLoadPerformance.test_load_query**


**$ FRONT=IP address python3 -m unittest -v test_load.TestLoadPerformance.test_load_buy**


**$ FRONT=IP address python3 -m unittest -v test_load.TestLoadPerformance.test_load_queryOrder**


You could check out the [output document](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/output.pdf) for details, the testing result could be like:


![load1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/load1.png)


    
## Caching Test Tutorial

    
**Caching Switch:** look at “front_end.py”, you can switch the state of caching by modifying the global variable “use_cach_flag”.

    
![cache](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/caching.png)    


The command you type on your local machine: 
    
    
**$ FRONT=IP address p=<probability> python3 client.py**


For each experiment with different p, we are testing multiple times, and record the average latency. The output screenshots for different p and caching state can be like this:


![cache1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/caching1.png)
    
 
    
## Fault Tolerance Test Tutorial


**Client Terminal:** we are sending 1000 buy requests using the code in load test.
    
    
**$ FRONT=IP address python3 -m unittest -v test_load.TestLoadPerformance.test_load_buy**


**Crash the follower with id = 1:** terminate the node with port = 10010 & id=1


![fault1](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault1.png)


**Restart the follower with id = 1:** restart the node with port = 10010 & id=1


![fault2](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault2.png)


**Crash the leader with id = 3:** since leader is crashed, front end performed the leader election, and notify other nodes who is the new leader. 


![fault3](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault3.png)

    
**New leader notification:** restart the node with port = 10010 & id=1


![fault4](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault4.png)
![fault5](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault5.png)

    
**Restart the follower with id = 3:** restart the node with port = 10012 & id=3


![fault6](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault6.png)
    

**Total latency seen by clients:**


![fault7](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault7.png)
       

**Order log at each order server:**


![fault8](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/figures/fault8.png) 
    

**In order to evaluate in what degree the clients can notice the failure, we do the same experiment without artificial crashes.**
    

You could check out the [evaluation document](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/evaluation%20document.pdf) for details.
    
    
## Way to Approach
Please check [design document](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/design%20document.pdf) for details.


## Simulation Results
Please check [Output](https://github.com/umass-cs677/lab3-spring22-yixiangzhang/blob/main/docs/output.pdf) for details.

