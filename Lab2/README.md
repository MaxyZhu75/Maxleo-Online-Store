# :whale: Maxleo Online Store - Lab 2



This lab has the following learning outcomes with regards to advanced concepts in distributed operating systems.
* Designed distributed server applications using a multi-tier architecture and microservices.
* Designed virtualized applications.
* Designed interfaces for web application.



The lab also has the following learning outcomes with regards to practice and modern technologies.
* Learned how to implement a REST API server.
* Learned how to measure the performance of a distributed application.
* Learned how to use Docker to containerize your micro-service, and learn to manage an application consisting of multiple containers using Docker Compose.
* Learned how to automatically test a distributed application.



# Part 1 - Implement Multi-Tiered Toy Store as Microservices



![part1](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/figures/part1/part1.jpg)



## Problem Statement



Here we simply summarize the responsibilities of each components as follows. Please check out the [Design Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/design/design%20document.pdf) for details.



### Client



It should be able to randomly queries an item, if the returned quantity is greater than 0, with probability “p” (environment variable initialized in terminal) it will send an order request.



* Mode 1: Query and buy randomly.



* Mode 2: Initiate a serials of Query.



* Mode 3: Initiate a serials of Buy.



### Front-end Server



Note that when implementing the front-end service, we did NOT use existing web frameworks such as Django, Flask, Spark, etc. Rather we design and implement our own functionalities.



* Interact with clients.



* Dispatch clients requests properly.



* Filter invalid bad requests.



### Catalog Server



We implemented the catalog server as an in memory but persistent on disk database. In other words, in our application, it is sort of like the Redis.



* Maintain data in memory & Persist data on disk.



* Process the “Buy” request from order server.



* Concurrency & Synchronization.



### Order Server



The order server will process all the “Buy” (POST) requests from the front-end server. It should communicate with catalog server during the process.



* Communicate with catalog server.



* Generate correct order ID.



* Write order log.



## Way to Approach



Please check out the [Design Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/design/design%20document.pdf) for details.



## Tutorial



Here we provide a tutorial for you to run and test our source code. Please check out the [Outputs Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/outputs/output.pdf) for details.



## Evaluation



We applied **Python Unittest Module** to test the functionality & load performance of the full application as well as the micro-services. The unittest unit framework supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.



Please check out the [Evaluation Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/evaluation/evaluation%20document.pdf) for details.



![evaluation](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/figures/part1/load2.png)




# Part 2 - Containerize Application with Docker



![part2](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/figures/part2/part2.jpg)



## Problem Statement



In this part, we will first containerize our application code, and then learn to deploy all components as a distributed application using Docker.



**Docker** provides the ability to package and run an application in a loosely isolated environment. The isolation and security allows us to run many containers simultaneously on a given host.



**Docker Compose** is a Docker tool which used to define and run multi-container applications. We use a YAML file to configure our application’s services, and then with a single command, we can create and start all the services from our configuration.



## Way to Approach
Please check out the [Design Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/design/design%20document.pdf) for details.



## Tutorial
Here we provide a tutorial for you to run and test our source code. Please check out the [Outputs Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/outputs/output.pdf) for details.



## Evaluation



We applied **Python Unittest Module** to test the functionality & load performance of the full application as well as the micro-services. The unittest unit framework supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.



Please check out the [Evaluation Document](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/evaluation/evaluation%20document.pdf) for details.



![evaluation](https://github.com/MaxyZhu75/Maxleo-Online-Store/blob/main/Lab2/summary/figures/part2/load2.png)



## :calling: Contact
Thank you so much for your interests. Note that this project can not straightforward be your course assignment solution. Do not download and submit my code without any change. Feel free to reach me out and I am happy to modify the Maxleo online store further with you.
* Email: maoqinzhu@umass.edu or zhumaxy@gmail.com
* LinkedIn: [Max Zhu](https://www.linkedin.com/in/maoqin-zhu/)
