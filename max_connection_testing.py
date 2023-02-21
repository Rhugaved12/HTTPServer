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


def send_request(inp, num):
    try:
        for i in range(num):
            if inp == 1:
                threading.Thread(target=GET_request_for_indexfile).start()
                threading.Thread(target=GET_request_for_html).start()
                threading.Thread(target=GET_request_for_binary).start()
                threading.Thread(target=GET_request_with_query).start()
                

            elif inp == 2:
                threading.Thread(target=HEAD_request_for_indexfile).start()
                threading.Thread(target=HEAD_request_for_html).start()
                threading.Thread(target=HEAD_request_for_binary).start()
                threading.Thread(target=HEAD_request_with_query).start()
                


            elif inp == 3:
                POST_request()

            elif inp == 4:
                PUT_request_for_text()
                PUT_request_for_binary()

            elif inp == 5:
                DELETE_request()
            
            else:
                print("Invalid Number entered")
                return
    except:
        print("Exception. Server has stopped working")
        exit()






def parse_response_status(status):
    if str(status) == '503':
        print('503\t>Connection Dropped')
    else:
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
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))

def GET_request_for_html():
    global count
    response = requests.get('http://localhost:' + str(port) + '/' + 'form.html')
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)

    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))

def GET_request_for_binary():
    global count
    global if_modified_since_time
    response = requests.get('http://localhost:' + str(port) + '/' + 'R1.png')
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # if_modified_since_time = headers['Last-Modified']
    # body = response.content
    # print(len(body))

def GET_request_with_query():
    global count
    response = requests.get('http://localhost:' + str(port) + '/' + 'form_submition_data.json', params={'fname': 'Rhugaved', 'lname': 'Narmade'} )
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))





def HEAD_request_for_indexfile():
    global count
    response = requests.head('http://localhost:' + str(port) + '/') 
    # count += 1
    # print(response, count)
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))

def HEAD_request_for_html():
    global count
    response = requests.head('http://localhost:' + str(port) + '/' + 'form.html')
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))

def HEAD_request_for_binary():
    global count
    global if_modified_since_time
    response = requests.head('http://localhost:' + str(port) + '/' + 'R1.png')
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # if_modified_since_time = headers['Last-Modified']
    # body = response.content
    # print(len(body))

def HEAD_request_with_query():
    global count
    response = requests.head('http://localhost:' + str(port) + '/' + 'form_submition_data.json', params={'fname': 'Rhugaved', 'lname': 'Narmade'}, )
    response.encoding = 'utf-8'
    status = response.status_code
    parse_response_status(status)
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))


def POST_request():
    # global count
    data = {"fname": "RRR", "mname": "JJJ", "lname": "NNN"}
    url='http://localhost:' + str(port) + '/' + 'form_data.json'
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
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))


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
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))


def DELETE_request():
    global count
    s = base64.b64encode('rhugaved:rn@123'.encode('utf-8')).decode('utf-8')
    # print(s.decode())

    fname = 'web.txt'
    response = requests.delete('http://localhost:' + str(port) + '/' + fname, headers={'Authorization': 'basic ' + s})
    response.encoding = 'utf-8'
    status = response.status_code
    print(parse_response_status(status))
    # headers = response.headers
    # print(parse_response_headers(headers))
    # body = response.content
    # print(parse_response_body(body))






if __name__ == "__main__":

    host = '127.0.0.1'
    port = 8800
    if len(sys.argv) > 1:
        port = sys.argv[1]
    try:
        num = int(input("Enter how many requests to send: "))
        inp = int(input("Enter which request to TEST:\nGET: 1\tHEAD: 2\tPUT: 3\tPOST: 4\tDELETE: 5\nEnter the Number: "))
        send_request(inp, num)


    except:
        print("Invalid input")

    







