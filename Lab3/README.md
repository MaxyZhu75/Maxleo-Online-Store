# :teddy_bear: Maxleo Online Store - Lab 3



This lab has the following learning outcomes with regards to advanced concepts in distributed operating systems.
* Designed caching, replication, and consistency.
* Designed fault tolerance and high availability.



The lab also has the following learning outcomes with regards to practice and modern technologies.
* Learned how to deploy our application on the AWS cloud.
* Learned how to measure the performance of a distributed application.
* Learned how to automatically test a distributed application.


# Part 1 - Caching, Replication and Fault Tolerance



![overview](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/figures/Overview.png)



## Problem Statement



This lab assignment is actually based on lab 2. We are further adding caching, replication, and fault tolerance to the micro-service toy store application. Please check out the [Design Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/design/design%20document.pdf) for details.



### Caching



We added caching to the front-end server to reduce the latency of the toy query requests. The front-end server start with an empty in-memory cache. Upon receiving a toy query request, it first checks the in-memory cache to see whether it can be served from the cache. If not, the request will then be forwarded to the catalog server, and the result returned by the catalog server will be stored in the cache.



Cache consistency needs to be addressed whenever a toy is purchased or restocked. We implemented a server-push technique: catalog server sends invalidation requests to the front-end server after each purchase and restock. The invalidation requests cause the front-end server to remove the corresponding item from the cache.



### Replication



In order to make our services more robust, this time we implemented order server as an order cluster. Like in previous lab, when we start the application, we first start the catalog server, but what’s different in this lab is we start 3 replicas of the order server, each with a unique id number and its own order log. In the cluster, there should always exists one node called leader, and the rest are called follower nodes.



Log consistency needs to be addressed too. In case of a successful buy (a new order number is generated), the leader node should propagate the information of the new order to other follower nodes.



### Fault Tolerance



Our goal is making sure that the online store application does not lose any order information due to crash failures. So the health check of each node in order cluster will be done by front-end server in our design. Only when it finds that the leader is unresponsive, it will redo the leader election according to the election rule. Furthermore, when a server in the cluster come back online from a crash, it should be able to pull the latest order log from other nodes in the cluster.



## Way to Approach



Please check out the [Design Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/design/design%20document.pdf) for details.



## Tutorial



Here we provide a tutorial for you to run and test our source code. Please check out the [Outputs Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/outputs/output.pdf) for details.



## Evaluation



We applied **Python Unittest Module** to test the functionality & load performance of the full application as well as the micro-services. The unittest unit framework supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.



Please check out the [Evaluation Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/evaluation/evaluation%20document.pdf) for details.



![evaluation](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/figures/func.png)




# Part 2 - Deployment on AWS



![part2](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/figures/aws3.png)



## Problem Statement



We are deploying our online application on an **m5a.large** instance in the us-east-1 region on AWS. Amazon Elastic Compute Cloud (EC2) provides scalable computing capacity in the Amazon Web Services (AWS) Cloud. Using Amazon EC2 eliminates our need to invest in hardware up front, so we can develop and deploy applications faster. We can use Amazon EC2 to launch as many or as few virtual servers as we need, configure security and networking, and manage storage.



## Way to Approach
Please check out the [Design Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/design/design%20document.pdf) for details.



## Tutorial
Here we provide a basic AWS Cloud deployment tutorial for you. Please check out the [Evaluation Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/evaluation/evaluation%20document.pdf) and [Outputs Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/outputs/output.pdf) for details.



## Evaluation



We simulated crash failures by killing a random order service replica while the clients is running, and then bring it back online after some time. In order to evaluate in what degree the clients can notice the failure, we do the same experiment without artificial crashes. And finally give our conclusion according to the packet loss rate, total latency, the number of lines in order log file, etc.



Please check out the [Evaluation Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/evaluation/evaluation%20document.pdf) for details.



![evaluation](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab3/summary/figures/aws2.png)



## :calling: Contact
Thank you so much for your interests. Note that this project can not straightforward be your course assignment solution. Do not download and submit my code without any change. Feel free to reach me out and I am happy to modify the Maxleo online store further with you.
* Email: maoqinzhu@umass.edu or zhumaxy@gmail.com
* LinkedIn: [Max Zhu](https://www.linkedin.com/in/maoqin-zhu/)
