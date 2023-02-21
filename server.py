import socket
import sys
import threading
import re
import os
import datetime
import mimetypes
import random
import string
from urllib.parse import parse_qs
import json
import base64
import pathlib

#MIMEtypes(content type), logging, config.py(for configuration file with username, password), webbrowser(For multithreading test case)
# for cookies, make a new cookie per client and when the same client makes a new request,
#  check if the cookie is present with us, and send the same cookie, don't send a different cookie to the same client. Use random library
#import webbrowser for simultaneous requests(open_new-tab funtion)
#maintain a list of running threads to check for max simultaneous connections and remove from list when closing the connection. 503 Service Unavailable for max simultaneous connections exceeded
#parse_qs: for parsing POST body: from urllib.parse import * 
#glob: In Python, the glob module is used to retrieve files/pathnames matching a specified pattern.  
 
# for testing use request module
# restman : chrome ext like postman
connected_clients = []
address_family = socket.AF_INET
socket_type = socket.SOCK_STREAM
request_queue_size = 5
# set request limit length
limit_request_length = 1024


#Maintain a dict for config file values
conf_dict = {}
conf_dict['MaxSimultaneousConnections'] = 10
conf_dict['access_log'] = 'log/access.log'
conf_dict['error_log'] = 'log/error.log'
conf_dict['log_level'] = 3
conf_dict['host'] = ''
conf_dict['port'] = 8800
conf_dict['DocumentRoot'] = os.getcwd()
conf_dict['username'] = 'rhugaved'
conf_dict['password'] = 'rn@123'





# Maintaining an acitve thread list to limit the number of active threads
active_threads = []
# MaxSimultaneousConnections = 10

# For DELETE Basic Authorization
# username = 'rhugaved'
# password = 'rn@123'

# Access log file name
# access_log = 'log/access.log'
# error_log = 'log/error.log'
# log_level = 3
max_log_info = ''

# host = ''
# port = 8800

# Document Route
# DocumentRoot = os.getcwd()

# To control the server
pause = False
stop = False


class webserver():
    # Class variable
    set_cookie = True
    cookie_size = 8
    # set Max-Age to 24 hours, set it as a string so that it can be concatenated later in the set-cookie response
    cookie_max_age = '86400' #Seconds in 24 hrs

    def __init__(self, client_connection, client_address):
        self.client_connection = client_connection
        self.client_address = client_address

        self.access_log_line = str(self.client_address[0])
        # print(self.access_log_line)
        self.uname = '-'


    def handle_request(self):
        global active_threads, max_log_info, conf_dict
        # active_threads.append(self.client_connection)
        # receive data from client and parse the request
        # while self.client+c
        # self.request_data = self.client_connection.recv(limit_request_length)
        # print(self.request_data)
        
        # self.request_data = b''



        # To receive bigger amount of data we use an array instead of a string, because
        # the append operation in an array is faster than '+' in a string
        fragments = []
        # receive data from client and parse the request
        while True:
            data = self.client_connection.recv(limit_request_length)
            # print(len(data))
            # self.request_data += data
            fragments.append(data)
            if len(data) < limit_request_length:
                # print("ENded")
                break
        # Here we join the array into an array
        self.request_data = b''.join(fragments)
        self.time_of_request = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %X GMT")

        if conf_dict['log_level'] in [1, 2, 3]:
            max_log_info += '[' +  self.time_of_request + '] ' + "Log Level: " + str(conf_dict['log_level']) + " New Connection: " + "[IP: " + str(self.client_address[0]) + " Port: " + str(self.client_address[1]) + "]" + "\n"
        if conf_dict['log_level'] == 3:
            max_log_info += str(self.client_address) + ' ' + "Length of request: " + str(len(self.request_data)) + "\n"
        
        initial_length_received = len(self.request_data)
        header = self.request_data.split(b'\r\n\r\n', 1)[0]
        header_length = len(header) + 4

        # print(initial_length_received, header_length)



        
        try:
            self.request_data = self.request_data.decode('utf-8')
            # print("No binary data")
            # set request body to None so that it can be parsed in the parse request function if it doesn't contain binary data
            self.request_body = None
            # print(len(self.request_body))
            self.binary_data = False
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Decoding the data" + "\n"

        except:
            # Means it contains binary data, then we split the received data at ('\r\n\r\n', 1) i.e separate head and body
            self.request_data = self.request_data.split(b'\r\n\r\n', 1)
            self.request_body = self.request_data[1]
            self.request_data = self.request_data[0].decode('utf-8')
            # print(len(self.request_body))
            self.binary_data = True
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Binary data present. Decoding the header data" + "\n"

        

        self.request_binary_data = None
        # print(self.request_data)
        # print('----------------')
        # print(self.byte_data[-100:-50])
        # print(len(self.request_body))


        # self.request_data = self.request_data.decode('utf-8')


        # self.request_data = base64.b64encode(self.request_data)
        # print(self.request_data)
        # print("=============")
        # self.request_data = base64.b64decode(self.request_data)
        # print(self.request_data)

        # If only a connection is created, but no request is made, close the connection so that only
        # when request is to be made the next time, new connection will be made
        if len(self.request_data) == 0:
            # print(self.request_data)
            # print(active_threads)

            active_threads.remove(self.client_connection)
            self.client_connection.close()
            # print(active_threads)
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "No content in the request. Closing the connection" + "\n\n"

            # Append to the error log file here
            with open(conf_dict['error_log'], 'a') as f:
                f.write(max_log_info)

            return


        # print(''.join(f'< {line}\n' for line in self.request_data.splitlines()))
        # print(self.request_data)



        # call parse request to get the request line
        self.parse_request()

        #call parse header to parse the request headers
        self.parse_header()


        if 'Content-Length' in self.header and int(self.header['Content-Length']) > initial_length_received - header_length:
            fragments = []
            # print(f"Initail: {initial_length_received},  Header: {header_length},  Total: {int(self.header['Content-Length'])}")
            size = int(self.header['Content-Length']) - initial_length_received - header_length
            # print("SIZE: ", size)
            # receive data from client and parse the request
            while size != 0:
                
                data = self.client_connection.recv(limit_request_length)
                # print(len(data))
                # self.request_data += data
                fragments.append(data)
                size -= len(data)
                # print("SIZE: ", size)
                if len(data) < limit_request_length:
                    # print("ENded")
                    break
            # Here we join the array into an array
            # print("Putside loop")
            d = b''.join(fragments)
            self.request_body += d
            # print("-=-=-=-=-=>>", len(self.request_body))
            # print(self.header['Content-Length'])




        # complete_request_body to use it later if required to find length of body etc
        self.complete_request_body = self.request_body

        




        # Check for the HTTP version to be 1.1
        if self.request_version != "HTTP/1.1":
            #505 HTTP Version not supported
            self.status = "505 HTTP Version Not Supported"

        #Respond according to the request_method
        if self.request_method == "GET":
            self.GET_response()

        elif self.request_method == "POST":
            self.POST_response()

        elif self.request_method == "HEAD":
            self.HEAD_response()

        elif self.request_method == "PUT":
            self.PUT_response()

        elif self.request_method == "DELETE": 
            self.DELETE_response()

        else:
            #400 Bad request
            response_bytes = 'HTTP/1.1 400 Bad Request\r\n'
            self.client_connection.send(response_bytes.encode('utf-8'))
            active_threads.remove(client_connection)
            self.client_connection.close()
            return
       
    def parse_request(self):
        global max_log_info, conf_dict

        '''
        split the request at newline. Eg of request: 
        GET /hello.html HTTP/1.1
        User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
        Host: www.tutorialspoint.com
        Accept-Language: en-us
        Accept-Encoding: gzip, deflate
        Connection: Keep-Alive

        request_body
        '''

        if conf_dict['log_level'] == 3:
            max_log_info += str(self.client_address) + ' ' + "Parsing the request" + "\n"


        # split at '\r\n\r\n' to seperate body and headers if it doesn't contain binary data
        if self.request_body is None:
            request = self.request_data.split('\r\n\r\n', 1)
            try:
                # storing request body. If request body is absent, exception will occur
                self.request_body = request[1]
                # print('No Binary body data, but with body')
            except:
                # print("No body")
                pass
            finally:
                # storing the request_data in an array
                self.request_array = request[0].splitlines()

        # If there is binary data in the reqeust, then the request_data holds the header data and reqeust_body already holds the body data
        else:
            # storing the request_data in an array
            self.request_array = self.request_data.splitlines()
        # print(request)
    
        
        

        


        #get the request line which is the first line in request
        request_line = self.request_array[0].rstrip('\r\n')
        if conf_dict['log_level'] in [1, 2, 3]:
            max_log_info += str(self.client_address) + ' ' + "Request Line: " + request_line + "\n"
        #Break down the request line into components
        (self.request_method,       #GET
        self.path,                  #/path
        self.request_version        #HTTP/1.1
        ) = request_line.split(" ")

        # Add Current working directory path
        self.parse_request_path()
        print(self.path)
        # print(conf_dict['DocumentRoot'])
        self.path = conf_dict['DocumentRoot'] + self.path
        # print(self.path)


    def parse_header(self):
        global max_log_info
        if conf_dict['log_level'] == 3:
            max_log_info += str(self.client_address) + ' ' + "Parsing the Request Headers" + "\n"
        # Forming a dictionary of the request header fields and storing it in self.header
        self.header = [
            element.rstrip("\r\n").split(": ") for element in self.request_array[1:]
        ]
        # Make self.header a dictionary of header fields present in request header without 
        # the request line(1st) and the request body
        self.header = {
            key: value for key, value in self.header
        }
        if conf_dict['log_level'] in [2, 3]:
            max_log_info += str(self.client_address) + ' ' + "Headers in the request:\n" + '\n'.join((f'[{key}]: {value}' for (key, value) in self.header.items())) + "\n"
        
        # print('=-='.join(
        #     f'{key}: {value}\n' for key, value in self.header.items()
        # )) 
        # print("--==>>", self.header['User-Agent'])
       


    def check_path(self):
        global max_log_info
        try:
            #check if path exists
            if not os.path.exists(self.path):
                # For POST request if the file doesn't exist, then make a new file and 
                # return status as 201 Created with the file location as the response body
                if self.request_method in ['POST', 'PUT']:
                    # First check if a file name is present at the end of the path
                    basename = os.path.basename(self.path)
                    if len(basename) > 0:
                        # Now check if the path without the filename exists
                        if os.path.exists(os.path.dirname(self.path)) and os.access(os.path.dirname(self.path), os.W_OK):
                            # Also check if the file is a .json file
                            try:
                                f = basename.split('.')[1]
                                # For POST
                                if f == 'json' and self.request_method == 'POST':
                                    self.post_file_data = open(self.path, 'w')
                                    self.status = "201 Created"
                                    self.file_data = b"File created successfully"
                                    
                                    if conf_dict['log_level'] == 3:
                                        max_log_info +=  str(self.client_address) + ' ' + 'File' + self.path + 'created Succesfully' + "\n"
                                    return
                                # For PUT no need to check file type, only check if there is a file and open the file in write+binary
                                if f and self.request_method == 'PUT':
                                    self.put_file_data = open(self.path, 'wb')
                                    self.status = "201 Created"
                                    # print('In created node=====')
                                    # For PUT there should not be any response body
                                    self.file_data = b'File Created Successfully'
                                    if conf_dict['log_level'] == 3:
                                        max_log_info += str(self.client_address) + ' ' + 'File' + self.path + 'created Succesfully' + "\n"
                                    return

                            except:
                                self.status = "500 Internal Server Error"
                                self.file_data = b"No file permission to Write"
                                if conf_dict['log_level'] == 3:
                                    max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Does not have permission to Write' + "\n"
                                return
                            
                        elif os.path.exists(os.path.dirname(self.path)) and not os.access(os.path.dirname(self.path), os.W_OK):
                            self.status = "500 Internal Server Error"
                            self.file_data = b"No file permission to Write"
                            if conf_dict['log_level'] == 3:
                                max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Does not have permission to Write' + "\n"
                            return

                                

                                

                #404 Not Found
                self.status = "404 Not Found"
                self.file_data = b'404 Not Found. Path does not exist'
                if conf_dict['log_level'] == 3:
                    max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Does not Exist' + "\n"
                return

            if os.path.isfile(self.path):
                #send the file data
                if self.request_method in ("GET", "HEAD"):
                    if os.access(self.path, os.R_OK):
                        self.file_data = open(self.path, 'rb')
                        self.file_data = self.file_data.read()
                        self.status = "200 OK"
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' read Succesfully' + "\n"
                        return
                    elif not os.access(self.path, os.R_OK):
                        self.status = "500 Internal Server Error"
                        self.file_data = b"No file permission to Read"
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Does not have permission to Write' + "\n"
                        return
                    

                elif self.request_method in ("POST"):
                    basename = os.path.basename(self.path)
                    f = basename.split('.')[1]
                    if f == 'json':
                        if os.access(self.path, os.W_OK):
                            self.post_file_data = open(self.path, 'a')
                            self.status = "200 OK"
                            self.file_data = b"Data stored successfully"
                            if conf_dict['log_level'] == 3:
                                max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Data stored Succesfully' + "\n"
                            return
                        elif not os.access(self.path, os.W_OK):
                            self.status = "500 Internal Server Error"
                            self.file_data = b"No file permission to Write"
                            if conf_dict['log_level'] == 3:
                                max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Does not have permission to Write' + "\n"
                            return

                elif self.request_method == 'PUT':
                    if os.access(self.path, os.W_OK):
                        self.put_file_data = open(self.path, 'wb')
                        self.status = "200 OK"
                        self.file_data = b"File written successfully"
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' can be accessed' + "\n"
                        return
                    elif not os.access(self.path, os.W_OK):
                        self.status = "500 Internal Server Error"
                        self.file_data = b"No file permission to Write"
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' Does not have permission to Write' + "\n"
                        return

                elif self.request_method == 'DELETE':
                    self.status = "204 No Content"
                    self.file_data = b''
                    if conf_dict['log_level'] == 3:
                        max_log_info +=  str(self.client_address) + ' ' + 'File ' + self.path + ' can be accessed' + "\n"
                    return




                        
                #Give error 403 Forbidden as the read/write permission is not available
                self.status = "403 Forbidden"
                self.file_data = b'403 Forbidden'
                if conf_dict['log_level'] == 3:
                    max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' cannot be accessed' + "\n"
                
                return

            elif os.path.isdir(self.path):

                if self.request_method in ("POST", 'PUT'):
                    # Check if this is okay. This is done because if a dir location is given
                    # then we can't open a file
                    self.status = "403 Forbidden"
                    self.file_data = b'403 Forbidden'
                    if conf_dict['log_level'] == 3:
                        max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' is actually a folder' + "\n"
                    return

                #send the index.html file if exists, else send error 404
                if not os.path.exists(self.path + 'index.html'):
                    #send error 404
                    self.status = "404 Not Found"
                    self.file_data = b'404 Not Found. File Not Found'
                    if conf_dict['log_level'] == 3:
                        max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' does not exist' + "\n"
                    return

                else:
                    #send the file index.html
                    self.path += 'index.html'
                    if self.request_method in ("GET", "HEAD"):
                        if os.access(self.path, os.R_OK):
                            """ 
                            print("---------file found----------")
                            print(self.path)
                            """
                            self.file_data = open(self.path, 'rb')
                            self.file_data = self.file_data.read()
                            self.status = "200 OK"
                            if conf_dict['log_level'] == 3:
                                max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + ' can be accessed' + "\n"
                            return
                        #Give error 403 Forbidden as the read permission is not available
                        self.status = "403 Forbidden"
                        self.file_data = b'403 Forbidden'
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + 'File ' + self.path + '     cannot be accessed' + "\n"
                        return
            
        except:
            self.status = '400 Bad Request'
            self.file_data = b'Error in file handling'


    def check_headers(self):
        global max_log_info, conf_dict
        try:
            if conf_dict['log_level'] in [2, 3]:
                max_log_info += str(self.client_address) + ' ' + "Checking Request headers" + "\n"
            # First need to check if the file is present and access is also available, to prevent errors while accessing file path(eg.Accept, ifs)
            if self.status not in ("404 Not Found", "403 Forbidden"):
                
                # ACCEPT: Check if the specific media type (eg. video/mp4) or all okay(*/*) or only primary type defined and present (eg. video/*)
                if 'Accept' in self.header and self.request_method in ['GET', 'HEAD', 'PUT']:
                    #check the header conditions present in the request header like if modified, accept etc.
                    content_type = mimetypes.guess_type(self.path)
                    self.accept()
                    if content_type not in self.accepted_media_types and '*/*' not in self.accepted_media_types and content_type.split('/')[0] + '/*' not in self.accepted_media_types:
                        self.status = "406 Not Acceptable" 
                        self.file_data = b"406 Not Acceptable"
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + "(Accept): Not acceptable content type" + "\n"

                    # if conf_dict['log_level'] == 3:
                    #     max_log_info += "(Accept): " + self.header['Accept'] + "\n"
                #HOST: If no host header is present respond with 400 (Bad Request)
                # if 'Host' in self.header:
                self.host()
                if conf_dict['log_level'] == 3:
                    max_log_info += str(self.client_address) + ' ' + "(Host): " + self.host + " is the host" + "\n"
                if self.host is None:
                    self.status = "400 Bad Request"
                    self.file_data = b"400 Bad Request. Host header not included"
                    if conf_dict['log_level'] == 3:
                        max_log_info += str(self.client_address) + ' ' + "(Host): Host Header not included" + "\n"
                

                if self.request_method in ['GET', 'HEAD'] and not self.query:
                    #IF-MODIFIED-SINCE: If the file has been modified after the time specified in the request, then send continue with the regular request.
                    # else if the file has not been modified, then send 304 NOT MODIFIED also, if the date given in the request is invalid(date format may be wrong 
                    # or the date may be later than servers current time), continue with regular GET
                
                    last_modified = os.path.getmtime(self.path)
                    # last_modified = datetime.datetime.fromtimestamp(last_modified, datetime.timezone.utc)
                    last_modified = datetime.datetime.fromtimestamp(last_modified, datetime.timezone.utc).replace(microsecond=0 ,tzinfo=None)

                    if 'If-Modified-Since' in self.header:
                        self.if_modified_since()
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + "(If-Modified-Since): Header present with time" + "\n"
                        if self.if_modified_since_time >= last_modified:
                            self.status = "304 Not Modified"
                            # The 304 response MUST NOT contain a message-body, and thus is always 
                            # terminated by the first empty line after the header fields. 
                            self.file_data = None
                    # IF-UNMODIFIED-SINCE: If the file has not been modified since the date given, then continue with the regular GET. 
                    # but if the file has been modified, then send 412 Precondition Failed. Also if the initial status is not 2XX ignore this header
                    # Also incase other IFs conditional GETs are used, then this is not defined
                    if 'If-Unmodified-Since' in self.header:
                        self.if_unmodified_since()
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + "(If-Unmodified-Since): Header present with time" + "\n"
                        if self.status == "200 OK" and self.if_unmodified_since_time < last_modified:
                            self.status = "412 Precondition Failed"
                            # The 412 response must send the error
                            self.file_data = b"412 Precondition Failed. Error in If-Modified-Sincse"

                if 'Cookie' in self.header:
                    self.cookie()
                

                # For POST and PUT Header:-
                if 'Content-Type' in self.header:
                    self.get_content_type()
                    if conf_dict['log_level'] == 3:
                        max_log_info += str(self.client_address) + ' ' + "(Content-Type): " + self.request_content_type + "\n"
                    
                    # print("*****", self.request_content_type)
                    if  'multipart/form-data' in self.request_content_type and self.request_method == 'POST':
                        # Content-Type: multipart/form-data; boundary=12345
                        self.request_content_type =  self.request_content_type.split('; boundary=')
                        self.post_boundary = self.request_content_type[1]
                        # Actual post_boundary
                        self.post_boundary = '--' + self.post_boundary
                        self.request_content_type = self.request_content_type[0]
                        # print("*****", self.post_boundary)

                else:
                    self.request_content_type = None

                
                    

            if 'User-Agent' in self.header:
                self.user_agent = self.header['User-Agent']
                # if conf_dict['log_level'] == 3:
                    # max_log_info += "(User-Agent): " + self.user_agent + "\n"
        except:
            self.status = '400 Bad Request'
            self.file_data = b'Error in header handling'
                    
                    

        
        
    # Parse the request body for POST(for now) and maybe PUT
    def parse_request_body(self):
        global max_log_info, conf_dict
        try:
            
            if self.status in ['200 OK', '201 Created']:
                if self.request_content_type == 'application/x-www-form-urlencoded':

                    # Check the content-length as well\
                    # If a request contains a message-body and a Content-Length is not given,
                    # the server SHOULD respond with 400 (bad request) if it cannot
                    # determine the length of the message, or with 411 (length required) if
                    # it wishes to insist on receiving a valid Content-Length.
                    if 'Content-Length' not in self.header:
                        self.status = '411 Length Required'
                        self.body = "Content-Length header is missing in the request"
                        return
                    else:
                        content_length = self.header['Content-Length']
                        if int(content_length) != len(self.complete_request_body):
                            self.status = '400 Bad Request'
                            self.body = "Content-Length header is present in the request, but does not match the real content length"
                            return

                    self.request_body = self.request_body.rstrip().lstrip()
                    # Converts the request body into a dictionary of name:value type
                    self.request_body_dict = parse_qs(self.request_body)

                    # print(self.request_body_dict)
                    # Write/append the request_body_data into the post_file_data which is a json file
                    if self.post_file_data.mode == 'w':
                        s = []
                        s.append(self.request_body_dict)
                        json.dump(s, self.post_file_data)
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + "Dumping the form data into the JSON file" + "\n"
                    elif self.post_file_data.mode == 'a':
                        with open(self.path, 'r') as f:
                            s = json.load(f)
                        
                        s.append(self.request_body_dict)
                        self.post_file_data.close()
                        self.post_file_data = open(self.path, 'w')
                        json.dump(s, self.post_file_data)
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + "Dumping the form data into the JSON file" + "\n"


                    # json.dump(self.request_body_dict, self.post_file_data)
                    self.post_file_data.close()




                elif self.request_content_type == 'multipart/form-data':
                    
                    if conf_dict['log_level'] == 3:
                        max_log_info += str(self.client_address) + ' ' + "Parsing the mulitpart/form-data" + "\n"
                    # print(f"----{self.content_type}----")
                    """Example: Here 
                    --boundary 
                    Content-Disposition: form-data; name="field1" 

                    value1 
                    --boundary 
                    Content-Disposition: form-data; name="field2"; filename="example.txt"
                    Content-Type: text/plain

                    value2
                    --boundary--"""
                    # Check the content-length as well\
                    # If a request contains a message-body and a Content-Length is not given,
                    # the server SHOULD respond with 400 (bad request) if it cannot
                    # determine the length of the message, or with 411 (length required) if
                    # it wishes to insist on receiving a valid Content-Length.
                    if 'Content-Length' not in self.header:
                        self.status = '411 Length Required'
                        self.body = "Content-Length header is missing in the request"
                        return
                    else:
                        if conf_dict['log_level'] == 3:
                            max_log_info += str(self.client_address) + ' ' + "Checking Content-Length" + "\n"
                        content_length = self.header['Content-Length']
                        # Calculate the content length
                        l = len(self.complete_request_body)
                        # print("++++++++", l)
                        # print(self.request_body)
                        if int(content_length) != l:
                            self.status = '400 Bad Request'
                            self.body = "Content-Length header is present in the request, but does not match the real content length"
                            return

                    # Check the Request Body(New)
                    body = ''
                    image = b''

                    

                    if self.binary_data and self.request_method == 'POST':
                        self.request_body_dict = {}
                        b = self.post_boundary + '\r\n'
                        b = b.encode('utf-8')
                        self.request_body = self.request_body.split(b)
                        for i in self.request_body:
                            if len(i) == 0:
                                #to skip '' which can be a entry as well in the list
                                continue
                            t = '\r\n' + self.post_boundary + '--'
                            t = t.encode('utf-8')
                            if t in i:
                                i.replace(t, b'')

                            v = i.split(b'\r\n\r\n')
                            if len(v) > 1:
                                value = v[1].lstrip().rstrip()
                                # print("-> ", value) 

                            i = v[0].decode('utf-8')
                            i = i.splitlines()
                            name = i[0]
                            pattern = "\"(.*?)\""
                            names_list = re.findall(pattern, name)
                            name = names_list[0]
                            # print(name, type(name))

                            if len(names_list) > 1:
                                # print("+++++Inside Saving File+++++")
                                file_name = names_list[1]
                                name = names_list[0]
                                # print(file_name, name)
                                # print(value)

                                # Create a file with the name given in the file_name and write the data
                                # in the file. Create the file in the POST_data folder
                                with open("POST_data/" + file_name, 'wb') as file_to_write:
                                    if conf_dict['log_level'] == 3:
                                        max_log_info += str(self.client_address) + ' ' + "Writing data to the Binary file mentioned in the FORM" + "\n"
                                    # if self.request_binary_data:
                                        # t = '\r\n' + self.post_boundary + '--'
                                        # t = t.encode('utf-8')
                                    # self.request_binary_data.replace(t, b'')
                                    file_to_write.write(value)
                                    # else:
                                    #     file_to_write.write(value.encode('utf-8'))

                                # Store the path of the file as the value in the JSON file
                                value = "POST_data/" + file_name
                                # print("-> -> ->", value)
                            else:
                                value = value.decode('utf-8')

                                
                            self.request_body_dict[name] = value
                            # print("->", value)

                        # print(f"+++++{self.request_body_dict}+++++")
                        # Write/append the request_body_data into the post_file_data which is a json file
                        if self.post_file_data.mode == 'w':
                            s = []
                            s.append(self.request_body_dict)
                            json.dump(s, self.post_file_data)
                        elif self.post_file_data.mode == 'a':
                            with open(self.path, 'r') as f:
                                s = json.load(f)
                            
                            s.append(self.request_body_dict)
                            # self.post_file_data.close()
                            self.post_file_data = open(self.path, 'w')
                            # print(s)
                            json.dump(s, self.post_file_data)
                            if conf_dict['log_level'] == 3:
                                max_log_info += str(self.client_address) + ' ' + "Dumping the data in the JSON file" + "\n"
                            
                        # json.dump(self.request_body_dict, self.post_file_data)
                        self.post_file_data.close()
                        return




                    # what i think is, save name: value fields in the data dic
                    # until a filename field is encountered and when a filename is 
                    # found, write all the data stored in the data dict into the file
                    # and clear the dict

                    # Here, if the data is just form data, then it contains a name and value only, 
                    # which can be added to the dictionary. But if it contains a file, like text or jpg,
                    # it also contains a filename which is the filename of the uploaded file and may also contain
                    # Content-Type field in the next line of name

                    self.request_body = self.request_body.rstrip().lstrip()
                    
                    self.request_body_dict = {}
                    self.request_body = self.request_body.split(self.post_boundary + '\r\n')
                    
                    # print(self.request_body)
                    for i in self.request_body:
                        if len(i) == 0:
                            #to skip '' which can be a entry as well in the list
                            continue
                            
                        # for the last entry, may contain extra boundary
                        if self.post_boundary + '--' in i:
                            i = i.replace('\r\n' + self.post_boundary + '--', '')
                        # if self.post_boundary in i:
                        #     i = i.replace('\r\n' + self.post_boundary, '')
                        
                        v = i.split('\r\n\r\n')
                        if len(v) > 1:
                            value = v[1].lstrip().rstrip()
                            # print("-> ", value)

                        i = v[0]
                        i = i.splitlines()
                        name = i[0]
                        pattern = "\"(.*?)\""
                        names_list = re.findall(pattern, name)
                        name = names_list[0]

                        if len(names_list) > 1:
                            # print("+++++Inside Saving File+++++")
                            file_name = names_list[1]
                            name = names_list[0]
                            # print(file_name, name)
                            # print(value)

                            # Create a file with the name given in the file_name and write the data
                            # in the file. Create the file in the POST_data folder
                            with open("POST_data/" + file_name, 'wb') as file_to_write:
                                if self.request_binary_data:
                                    t = '\r\n' + self.post_boundary + '--'
                                    t = t.encode('utf-8')
                                    self.request_binary_data.replace(t, b'')
                                    file_to_write.write(self.request_binary_data)
                                else:
                                    file_to_write.write(value.encode('utf-8'))

                            # Store the path of the file as the value in the JSON file
                            value = "POST_data/" + file_name
                            # print("-> -> ->", value)
                            
                        self.request_body_dict[name] = value

                    # print(f"+++++{self.request_body_dict}+++++")
                    # Write/append the request_body_data into the post_file_data which is a json file
                    if self.post_file_data.mode == 'w':
                        s = []
                        s.append(self.request_body_dict)
                        json.dump(s, self.post_file_data)
                    elif self.post_file_data.mode == 'a':
                        with open(self.path, 'r') as f:
                            s = json.load(f)
                        
                        s.append(self.request_body_dict)
                        self.post_file_data.close()
                        self.post_file_data = open(self.path, 'w')
                        json.dump(s, self.post_file_data)
                        
                    # json.dump(self.request_body_dict, self.post_file_data)
                    self.post_file_data.close()
        except:
            self.status = '400 Bad Request'
            self.file_data = b'Error in handling POST request'

        
       


        
    # Get the response head to send with the response
    def start_response(self):
        global max_log_info
        self.current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %X GMT")
        self.server_response_header = [('Date', self.current_time)]
        self.server_version = "111803084/1.0 (Linux)"
        self.server_response_header.append(('Server', self.server_version))
        self.connection = 'close'
        self.server_response_header.append(('Connection', self.connection))
        self.content_length = 0

        if self.status in ["200 OK", "201 Created"]:

            if self.request_method in ['GET', 'HEAD'] and not self.query:
                #check the self.path here. It might not be file path, it may be a directory or something, or maybe we need to specify index.html file path
                self.last_modified = os.path.getmtime(self.path)
                self.last_modified = datetime.datetime.fromtimestamp(self.last_modified, datetime.timezone.utc).strftime("%a, %d %b %Y %X GMT")
                self.server_response_header.append(('Last-Modified', self.last_modified))
                #check the self.path here too. Check above comment
                self.content_length = os.path.getsize(self.path)
                self.server_response_header.append(('Content-Length', self.content_length))
                #content type to be given and other headers to be added
                self.content_type = mimetypes.guess_type(self.path)[0]
                self.content_type += '; charset=UTF-8'
                self.server_response_header.append(('Content-Type', self.content_type))

            elif self.request_method in ['POST']:
                self.content_length = len(self.file_data) 
                self.server_response_header.append(('Content-Length', self.content_length))

                self.content_type = 'text/plain' + '; charseet=UTF-8'
                self.server_response_header.append(('Content-Type', self.content_type))

            # If self.set_cookie is True, then either the client has connected for the first time or the cookie has expired
            if self.set_cookie:
                self.set_cookie_value = 'cookie_id=' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.cookie_size)) + '; ' + 'Max-Age=' + self.cookie_max_age
                self.server_response_header.append(('Set-Cookie', self.set_cookie_value))
        
        else:
            self.server_response_header = [
                ('Date', self.current_time), 
                ('Server', self.server_version),
                ('Connection', self.connection)
            ]

        
    # Collect all the data and send it to the client
    def finish_response(self):
        global max_log_info
        global active_threads
        global conf_dict
        try:
            response = f'HTTP/1.1 {self.status}\r\n'
            for header in self.server_response_header:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            # response = b''.join((response, self.file_data))
            # response += self.file_data

            #print formatted response data
            # print(''.join(
            #     f'> {line}\n' for line in response.splitlines()
            # ))

            # print("====>>>>", self.user_agent)

            # Writing the access log file
            self.access_log_line +=  ' ' + self.uname + ' ' + "[" + str(self.time_of_request) + "]" + ' \"' + ' '.join(i for i in self.request_array[0].rstrip('\r\n').split(' ')) + '\" ' + self.status + ' ' + "[" + str(self.content_length) + "]" + ' ' + self.user_agent + '\n'
            print("--->>> ", self.access_log_line)


            if conf_dict['log_level'] in [2, 3]:
                max_log_info += str(self.client_address) + ' ' + "Response Headers: " + "\n"
                max_log_info += '\n'.join( f'> {line}' for line in response.splitlines())

            if conf_dict['log_level']== 1:
                max_log_info += str(self.client_address) + ' ' + "Reponse Status: " + ' \"' + self.status + ' \"' + "\n\n"

            with open(conf_dict['access_log'], 'a+') as log:
                log.write(self.access_log_line)
           


            response_bytes = response.encode()

            if self.file_data:
                if conf_dict['log_level'] == 3:
                    max_log_info += str(self.client_address) + ' ' + "Appending Response Body" + "\n"
                response_bytes += self.file_data

            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Sending Response" + "\n"
            self.client_connection.send(response_bytes)
            
            # if self.status == "200 OK":
            # print(self.file_data)
            #Do not send file date for HEAD request
            # if self.request_method != 'HEAD' and self.file_data is not None:
            #     self.client_connection.send(self.file_data)

        finally:
            # print(active_threads)
            active_threads.remove(self.client_connection)
            self.client_connection.close()
            # print(active_threads)
            if conf_dict['log_level'] in [2, 3]:
                max_log_info += str(self.client_address) + ' ' + "Closing the connection and the thread" + "\n\n"

            with open(conf_dict['error_log'], 'a') as f:
                f.write(max_log_info)




    def parse_request_path(self):
        global max_log_info, conf_dict
        try:
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Parsing the Request Path" + "\n"

            p = 'http://localhost:' + str(conf_dict['port'])
            if p in self.path:
                self.path = self.path.replace(p, '')
                # print(self.path)

            s = self.path.split('?')
            self.path = s[0]
            if len(s) > 1:
                if conf_dict['log_level'] == 3:
                    max_log_info += str(self.client_address) + ' ' + "Conditional GET Present" + "\n"
                self.query = {}
                # self.query = parse_qs(s[1])
                q = s[1].split('&')
                for i in q:
                    j = i.split('=')
                    self.query[j[0]] = j[1]

                # print(self.query)

            else:
                self.query = None
            # print(self.query)
        except:
            self.status = '500 Internal Server Error'
            self.file_data = b'Server Error'
            
        

    def accept(self):
        try:
            accept = self.header['Accept']
            # Use RegEx to split the media types without condidering q values
            pattern = ';q=\d\.\d,|;q=\d,|;q=\d\.\d|;q=\d'
            accept = re.split(pattern, accept)
            accept = [i.split(',') for i in accept if len(i) > 0]
            self.accepted_media_types = []
            for i in accept:
                for j in i:
                    self.accepted_media_types.append(j)
            # print("In Accept")
            return
        except:
            return

    def host(self):
        try:
            self.host = self.header['Host'] 
        except:
            self.host = None

    def if_modified_since(self):
        time = self.header['If-Modified-Since']
        try:
            self.if_modified_since_time = datetime.datetime.strptime(time, "%a, %d %b %Y %X %Z")
        except:
            self.if_modified_since_time = None

    def if_unmodified_since(self):
        time = self.header['If-Unmodified-Since']
        try:
            self.if_unmodified_since_time = datetime.datetime.strptime(time, "%a, %d %b %Y %X %Z")
        except:
            self.if_unmodified_since_time = None

    def cookie(self):
        global max_log_info, conf_dict
        try:
            cookie = self.header['Cookie']
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "(Cookie): " + str(cookie) + " already present"+ "\n"
            # set Max-Age to 24 hours: Not using this to update the cookie expiry for now.
            # self.cookie_max_age = '3576' #24 Hrs in secs
            self.set_cookie = False

        except:
            self.set_cookie = True
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Cookie to be set" + "\n"
        
    # For POST
    def get_content_type(self):
        try:
            self.request_content_type = self.header['Content-Type']
        except:
            if self.request_method == 'POST':
                self.request_content_type = "application/x-www-form-urlencoded"
            if self.request_method == 'PUT':
                self.request_content_type = None

    # Mainly for DELETE
    def authorization(self):
        try:
            global max_log_info, conf_dict
            auth = self.header['Authorization']
            auth = auth.split(' ')
            auth_type = auth[0]
            credentials = auth[1]
            # print(credentials)
            credentials = base64.b64decode(credentials).decode('utf-8')
            # print(credentials)
            credentials = credentials.split(':')
            # needed for the access log file
            self.uname = credentials[0]
            self.passd = credentials[1]
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "(Authorization): " + "Username: " + self.uname + "Password: " + self.passd + "\n"

            if conf_dict['username'] != self.uname or conf_dict['password'] != self.passd:
                self.status = "401 Unauthorized"
                self.body = "Authorization Failed"
                if conf_dict['log_level'] == 3:
                    max_log_info += str(self.client_address) + ' ' + "Authorization Failed" + "\n"
            
        except:
            self.status = "401 Unauthorized"
            self.body = "Authorization Failed"
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Authorization Failed" + "\n"
            
        




    def GET_response(self):
        global max_log_info, conf_dict
        try:
            if conf_dict['log_level'] in [2, 3]:
                max_log_info += str(self.client_address) + ' ' + "Request method: GET" + "\n"
            # print('inside get methodZ')
            # Check the path first
            self.check_path()
            # Check the request headers
            self.check_headers()
            # Make the response header
            self.start_response()

            # Check if the GET is query GET and check if the file is .json
            # print(self.query, pathlib.Path(self.path).suffix)
            if self.query and self.status == '200 OK':
                if pathlib.Path(self.path).suffix == '.json':
                    with open(self.path, 'r') as f:
                        data = json.load(f)
                        self.file_data = []
                        for d in data:
                            # s is T/F if the query is a subset of the dictionary
                            s = all(item in d.items() for item in self.query.items())
                            if s:
                                self.file_data.append(d)
                            
                    # Dumps converts the python list to a json string which needs to encoded before final_response
                    self.file_data = json.dumps(self.file_data).encode('utf-8')
                    self.content_length = len(self.file_data) 
                    self.server_response_header.append(('Content-Length', self.content_length))
                    # print("=+=+=+=+")
                    # print(self.file_data)
                    if conf_dict['log_level'] == 3:
                        max_log_info += str(self.client_address) + ' ' + "Queried GET: " + str(self.query) + "\n"
                    self.content_type = 'application/json' + '; charseet=UTF-8'
                    self.server_response_header.append(('Content-Type', self.content_type))
        except:
            self.status = '400 Bad Request'
            self.file_data = b'GET request Error'
        # Finish Response
        # print("====>>>>", self.user_agent)

        self.finish_response()
        return

    def HEAD_response(self):
        global max_log_info, conf_dict
        if conf_dict['log_level'] in [2, 3]:
            max_log_info += str(self.client_address) + ' ' + "Request method: HEAD" + "\n"
        #Same as GET, just do not send the message body with the response
        # Check the path first
        self.check_path()
        # Check the request headers
        self.check_headers()
        # Make the response header
        self.start_response()
        # Finish Response
        self.finish_response()
        return

    def POST_response(self):
        global max_log_info, conf_dict
        if conf_dict['log_level'] in [2, 3]:
            max_log_info += str(self.client_address) + ' ' + "Request method: POST" + "\n"
        # First check the path in URI. If its a form submission and the file is not present on the server
        # create the file and send 201 created response along with the file path in the response body.
        # If the file is present, then first chech the file permissions and then open the file in append form and then
        # write the parsed data received through the body of POST request
        # Check the path first
        self.check_path()
        # # Check the request headers
        self.check_headers()
        


        # # Work on the request_body
        self.parse_request_body()

        #start response
        self.start_response()
        # finish response
        self.finish_response()


    def PUT_response(self):
        global max_log_info, conf_dict
        if conf_dict['log_level'] in [2, 3]:
            max_log_info += str(self.client_address) + ' ' + "Request method: PUT" + "\n"
        # Similar to POST, only instead of appending to the file, we write(200 Ok) into the file at the location
        # provided in the uri. If the uri does not exist, then check if that uri can represent a file, and if so 
        # then create the file(201 Created)
        self.check_path()
        self.check_headers()

        try:
            content_length = self.header['Content-Length']
        except:
            pass

        if self.request_content_type is None:
            self.status = '400 Bad Request'
            self.file_data = b'400 Bad Request. Content type not provided'
        else:
            c = mimetypes.guess_type(self.path)[0]
            # print("Content type")
            # print(c, self.request_content_type)
            # print("type of content")
            # print(type(c), type(self.request_content_type))
            if c != self.request_content_type:
                self.status = '400 Bad Request'
                self.file_data = b'400 Bad Request. Content type not correct'

            elif 'Content-Length' not in self.header:
                    self.status = '411 Length Required'
                    self.file_data = b"Content-Length header is missing in the request"
                    
            if int(content_length) != len(self.complete_request_body):
                self.status = '400 Bad Request'
                self.file_data = b"Content-Length header is present in the request, but does not match the real content length"

            else:
                # print("In PUT else")
                # print(len(self.request_body))
                if type(self.request_body) == bytes:
                    self.put_file_data.write(self.request_body)
                    self.put_file_data.close()
                else:
                    self.put_file_data.write(self.request_body.encode('utf-8'))
                    self.put_file_data.close()

        # print("IN PUT: ", self.status)
        self.start_response()
        self.finish_response()


    def DELETE_response(self):
        global max_log_info, conf_dict
        if conf_dict['log_level'] in [2, 3]:
            max_log_info += str(self.client_address) + ' ' + "Request method: DELETE" + "\n"
        # First check the path of the file (If folders can be deleted or not is not decided yet)
        # Check for Authorization header, and check for the username and password. Basic authorization and
        # the credentials are Base64 encoded.
        self.check_path()
        self.check_headers()
        # For DELETE mainly
        if 'Authorization' not in self.header and self.status in ['200 OK', '204 No Content', '202 Accepted']:
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Authorization Not Present" + "\n"
            self.status = "401 Unauthorized"
            self.body = "Authorization Failed"
            
        elif 'Authorization' in self.header and self.status in ['200 OK', '204 No Content', '202 Accepted']:
            if conf_dict['log_level'] == 3:
                max_log_info += str(self.client_address) + ' ' + "Checking Authorization" + "\n"
            self.authorization()

        if self.status in ['200 OK', '204 No Content', '202 Accepted']:
            try:
                os.remove(self.path)
            except:
                self.status = '403 Forbidden'
                self.file_data = b'Could not delete'

        self.start_response()
        self.finish_response()
                



#first called funtion to get requests from clients by making a server object
def make_server(client_connection, client_address):
    global active_threads
    global conf_dict
    global max_log_info
    # print(active_threads)
    server = webserver(client_connection, client_address)
    if conf_dict['log_level'] == 2:
        max_log_info = str(self.client_address) + ' ' + 'Connected to ' + str(client_connection)
    server.handle_request()
    return


def action():
    global pause, stop
    
    while True:
        # print(pause, stop)
        state = input()
        if state.lower() == 'stop':
            stop = True
            # print("inside stop", stop)
            break
        elif state.lower() == 'pause':
            pause = True
            # print(pause)
        elif state.lower() == 'restart':
            pause = False
        else: 
            continue
    print("Stop the server. Server will stop after one more client is connected")
                


def config_parser():
    global conf_dict
    with open("setup.config", 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                # print(len(line))     
                # continue       
                if line[0] == '#':
                    # print(line)
                    pass
                else:
                    try:
                        l = line.split('=')
                        # continue
                        l[0] = l[0].strip()
                        l[1] = l[1].strip()
                        conf_dict[l[0]] = l[1]
                        # print(l)
                    except:
                        print("Invalid Sytax in Config file")
                        conf_dict.clear()
                        break

        conf_dict['port'] = int(conf_dict['port'])
        conf_dict['log_level'] = int(conf_dict['log_level'])
        conf_dict['MaxSimultaneousConnections'] = int(conf_dict['MaxSimultaneousConnections'])

        # print("IN FUNCTION:", conf_dict)




if __name__ == "__main__":

    print("Server is running:")

    config_parser()

    #make a socket instance and pass 2 parameters. AF_NET: ipv4 family and SOCK_STREAM: TCP Protocol
    try: 
        s = socket.socket(address_family, socket_type)
        print("Socket Created Succesfully")

    except socket.error:
        print("Socket creation failed due to error", socket.error)

    s.bind((conf_dict['host'], conf_dict['port']))
    print("Socket binded to port: ", conf_dict['port'])

    #Socket in listening mode
    s.listen(request_queue_size)
    print("Socket is listening")

    # global pause, stop
    # print("pause: and stop: ", pause, stop)

    # make a thread to take the inputs for controlling the server
    threading.Thread(target=action).start()

    #Infinite loop to accept requests
    #ADD start, stop and close flags
    count = 1
    while not stop:
        if not pause:
            # print(stop)
            #establish a connection with one client at a time
            client_connection, client_address = s.accept()
            # print(count)
            count += 1

            #store the client info in the array connected_clients
            connected_clients.append(client_connection)

            print("Connected to: ", client_address)

            #Make a thread per client
            active_threads.append(client_connection)
            if len(active_threads) <= conf_dict['MaxSimultaneousConnections']:
                threading.Thread(target=make_server, args=(client_connection, client_address, )).start()
            else:
                # print(active_threads)
                response_bytes = "HTTP/1.1 503 Service Unavailable\r\n"
                # print(response_bytes)

                
                fragments = []
                # receive data from client and parse the request
                while True:
                    data = client_connection.recv(limit_request_length)
                    # print(len(data))
                    # self.request_data += data
                    fragments.append(data)
                    if len(data) < limit_request_length:
                        # print("ENded")
                        break
                client_connection.send(response_bytes.encode('utf-8'))
                active_threads.remove(client_connection)
                client_connection.close()

        else:
            
            continue

    s.close()
    print('Closed')



    