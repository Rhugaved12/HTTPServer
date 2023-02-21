MIS: 111803084
Name: Rhugaved Narmade
Div: 1
Project name: HTTP Server


How to run the server:
$python3 server.py

How to run the client testing program:
First run the server with: $python3 server.py
Then, run the testing file
-> Give port_no according to what is configured in the setup.config file
$python3 client_testing.py port_no

How to run the max_connection_testing program:
First run the server with: $python3 server.py
Then, run the testing file
-> Give port_no according to what is configured in the setup.config file
$python3 max_connection_testing.py port_no

Check and configure the setup.config file before running the server. If some fields are empty in the config file, then the server will use default values

Server Start-Pause-Restart-Stop
First run server using "python3 server.py". The server is constantly waiting for input from the user on the terminal.
Pause: Temporarily pauses the furthur acceptance of requests
Restart: Continues the paused server to accept the requests
Stop: Waits for one final request, and closes/stops the server

Methods Implemented with appropriate status codes:
-> File permissions are appropriatly handled by every request
-> Most of the header are also handled
1. GET:
    1. All types of files can be requested from the server(text, binary etc)
    2. Conditional GET has also been Implemented
    3. Queried GET request is also handled by the server. (Can only be used to get data from .JSON file)

2. HEAD:
    All the methods as implemented in GET work for the HEAD request as well

3. POST:
    (Stored data in a .JSON file only as mentioned in the action attribute of the form)
    1. Handles "application/x-www-form-urlencoded" form data and stores the data in a .JSON file
    2. Handles "multipart/form-data" form data and stores in a .JSON file. This type of form can handle any type of multiple file input in the form like text, binary files like images, pdf etc of any length

4. PUT:
    1. Handles any type of file data of any length

5. DELETE:
    1. Deleted all type of files
    2. Authorization is required (Check setup.config for the username and password. Do not change the username and password in config file is you are going to use testing program)
    

Config file specifications:
1. Use '#' to comment
2. Format of data storage: key = value
3. Check setup.config for more info

Logging:
1. Access log: Stores info about the connected clients with Apache like Format
2. Error log: 3 levels: 1, 2, 3 in the increasing order of detailness
3. Log file locations can be given in the config file

Cookies:
1. When a new page is requested, a cookie is set for the client with a Max-Age
2. Checks if there is cookie header when the same client is connected again




