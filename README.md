# :elephant: Maxleo Online Store



This project is from UMass Amherst Computer Science department. It provides an in-depth examination of the principles of distributed systems and advanced concepts in operating systems. Specifically, there are totally 3 lab assignments in this repository, covering topics include client-server programming, producer-consumer problem, gRPC framework, microservices architecture, handwritten HTTP frameworks, REST APIs, virtualization, Docker, caching, distributed scheduling, cluster fault tolerance, AWS Cloud, automated testing, etc.



## Lab1
In this part, we implemented an online Toy store as a socket-based client-server application. Our design should be able multiple client processes making **concurrent requests to the server.** The main part of the assignment is to **implement our own ThreadPool** (not allowed to use a ThreadPool framework that are available by the language/libraries).

The server component should implement a single method Query, which takes a single string argument that specifies the name of the toy. The Query method returns the dollar price of the item (as a floating point value such as 25.99) if the item is in stock. It returns -1 if the item is not found and 0 if the item is found but not in stock. The client component should connect to the server using a socket connection. It should construct a message in the form of a buffer specifying the method name (e.g., string "Query") and arguments ("toyName"). The message is sent to the server over the socket connection. The return value is another buffer containing the cost of the item or an error code such as -1 and 0, as noted above.



## Lab2
Please check out the [Design Document](https://github.com/MaxyZhu75/Toy-Store/blob/main/summary/design/design%20document.pdf) for details.



## Lab3
How to run and test our code? Here we provide examples of functional test & load test. Please check out the [Outputs Document](https://github.com/MaxyZhu75/Toy-Store/blob/main/summary/outputs/output.pdf) for details.



## :calling: Contact
Thank you so much for your interests. Note that this project can not straightforward be your course assignment solution. Do not download and submit my code without any change. Feel free to reach me out and I am happy to modify this online toy store further with you.
* Email: maoqinzhu@umass.edu or zhumaxy@gmail.com
* LinkedIn: [Max Zhu](https://www.linkedin.com/in/maoqin-zhu/)
