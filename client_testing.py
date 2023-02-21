import socket
import threading
import sys
import requests
import mimetypes
import base64

count = 0
if_modified_since_time = 0
if_unmodified_since_time = 0
port = 8800


def send_request(inp):
    # for i in range(10):
    try:
        if inp == 1:
            
            GET_request_for_indexfile()
            GET_request_for_html()
            GET_request_for_binary()
            GET_request_with_query()
            GET_request_with_ifmodifiedsince()
            GET_request_with_ifunmodifiedsince()

        elif inp == 2:
            
            HEAD_request_for_indexfile()
            HEAD_request_for_html()
            HEAD_request_for_binary()
            HEAD_request_with_query()
            HEAD_request_with_ifmodifiedsince()
            HEAD_request_with_ifunmodifiedsince()


        elif inp == 3:
            POST_request_with_files()
            POST_request_without_file()

        elif inp == 4:
            PUT_request_for_text()
            PUT_request_for_binary()

        elif inp == 5:
            DELETE_request()
        
        else:
            print("Please enter a number as shown above")
            
        return
    
    except:
        print("Exception. Server has stopped working")
        exit()



def parse_response_status(status):
    print(status)

def parse_response_headers(headers):
    for key, value in headers.items():
        print(f'{key}: {value}')

def parse_response_body(body):
    print(body)

def GET_request_for_indexfile():
    global count
    response = requests.get('http://localhost:' + str(port) + '/') 
    # count += 1
    # print(response, count)
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))

def GET_request_for_html():
    global count
    response = requests.get('http://localhost:' + str(port) + '/' + 'form.html')
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))

def GET_request_for_binary():
    global count
    global if_modified_since_time
    response = requests.get('http://localhost:' + str(port) + '/' + 'R1.png')
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    if_modified_since_time = headers['Last-Modified']
    body = response.content
    print(len(body))

def GET_request_with_query():
    global count
    response = requests.get('http://localhost:' + str(port) + '/' + 'form_submition_data.json', params={'fname': 'Rhugaved', 'lname': 'Narmade'}, )
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))

# Call only after calling Binary GET
def GET_request_with_ifmodifiedsince():
    global count
    global if_modified_since_time
    response = requests.get('http://localhost:' + str(port) + '/' + 'R1.png', headers={'If-Modified-Since': if_modified_since_time})
    response.encoding = 'utf-8'
    status = response.status_code
    print("+++", parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(len(body))

# Call only after calling Binary GET
def GET_request_with_ifunmodifiedsince():
    global count
    global if_modified_since_time
    response = requests.get('http://localhost:' + str(port) + '/' + 'R1.png', headers={'If-Unmodified-Since': if_modified_since_time})
    response.encoding = 'utf-8'
    status = response.status_code
    print("---", parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(len(body))





def HEAD_request_for_indexfile():
    global count
    response = requests.head('http://localhost:' + str(port) + '/') 
    # count += 1
    # print(response, count)
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))

def HEAD_request_for_html():
    global count
    response = requests.head('http://localhost:' + str(port) + '/' + 'form.html')
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))

def HEAD_request_for_binary():
    global count
    global if_modified_since_time
    response = requests.head('http://localhost:' + str(port) + '/' + 'R1.png')
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    if_modified_since_time = headers['Last-Modified']
    body = response.content
    print(len(body))

def HEAD_request_with_query():
    global count
    response = requests.head('http://localhost:' + str(port) + '/' + 'form_submition_data.json', params={'fname': 'Rhugaved', 'lname': 'Narmade'}, )
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))

# Call only after calling Binary HEAD
def HEAD_request_with_ifmodifiedsince():
    global count
    global if_modified_since_time
    response = requests.head('http://localhost:' + str(port) + '/' + 'R1.png', headers={'If-Modified-Since': if_modified_since_time})
    response.encoding = 'utf-8'
    status = response.status_code
    print("+++", parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(len(body))

# Call only after calling Binary HEAD
def HEAD_request_with_ifunmodifiedsince():
    global count
    global if_modified_since_time
    response = requests.head('http://localhost:' + str(port) + '/' + 'R1.png', headers={'If-Unmodified-Since': if_modified_since_time})
    response.encoding = 'utf-8'
    status = response.status_code
    print("---", parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(len(body))


def POST_request_with_files():
    # global count
    fname2 = 'R1.png'
    f2 = open(fname2, 'rb')

    fname = 'z.jpg'
    f = open(fname, 'rb')

    # content_type = mimetypes.guess_type(fname)[0]
    files = {'fileToUpload': f, 'file2Upload': f2}
    data = {"fname": "RRR", "mname": "JJJ", "lname": "NNN"}
    url='http://localhost:' + str(port) + '/' + 'form_submition_data.json'
    # print(url)
    response = requests.post(url=url, data=data, files=files)
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers  
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))


def POST_request_without_file():
    # global count
    data = {"fname": "RRR", "mname": "JJJ", "lname": "NNN"}
    url='http://localhost:' + str(port) + '/' + 'form_submition_data.json'
    # print(url)
    response = requests.post(url=url, data=data)
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers  
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))




def PUT_request_for_text():
    global count
    fname = 't.txt'
    with open(fname, 'rb') as f:
        content_type = mimetypes.guess_type(fname)[0]
        # print(content_type)
        data = f.read()
    response = requests.put('http://localhost:' + str(port) + '/' + 'put' + fname, data=data, headers={'Content-Type': content_type})
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))


def PUT_request_for_binary():
    global count
    fname = 'testing.pdf'
    with open(fname, 'rb') as f:
        content_type = mimetypes.guess_type(fname)[0]
        # print(content_type)
        data = f.read()
    response = requests.put('http://localhost:' + str(port) + '/' + 'put' + fname, data=data, headers={'Content-Type': content_type})
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))


def DELETE_request():
    global count
    credentials = base64.b64encode('rhugaved:rn@123'.encode('utf-8')).decode('utf-8')
    # print(s.decode())
    fname = 'web.txt'
    response = requests.delete('http://localhost:' + str(port) + '/' + fname, headers={'Authorization': 'basic ' + credentials})
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    headers = response.headers
    print(parse_response_headers(headers))
    body = response.content
    print(parse_response_body(body))






if __name__ == "__main__":

    host = '127.0.0.1'
    port = 8800
    if len(sys.argv) > 1:
        port = sys.argv[1]
    inp = int(input("Enter which request to TEST:\nGET: 1\tHEAD: 2\tPOST: 3\tPUT: 4\tDELETE: 5\tTo quit testing: 0\nEnter the Number: "))
    while inp != 0:
        send_request(inp)
        inp = int(input("Enter which request to TEST:\nGET: 1\tHEAD: 2\tPOST: 3\tPUT: 4\tDELETE: 5\tTo quit testing: 0\nEnter the Number: "))







