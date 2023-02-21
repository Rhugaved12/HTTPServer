import datetime, os, mimetypes, re, chardet, logging, json, stat, base64
from urllib.parse import parse_qs

# t = os.path.getmtime("/TYCourses")
# t = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
# print(t.strftime("%a, %d %b %Y %X GMT"))

# print(datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %X GMT"))
# #Sun, 18 Oct 2012 10:36:20 GMT

# f = open('/home/rhugaved/t.txt', "r")
# print(len(f.read()))
# print(os.path.getsize("//home/rhugaved/t.txt"))

# print(mimetypes.guess_type("/home/rhugaved/t.txt"))

# arr = [['a', 1], ['b', 2]]
# for x, y in arr:
#     print(x, y)


""" accept = "text/html, mp3/song"
pattern = ';q=\d\.\d,|;q=\d,|;q=\d\.\d|;q=\d'
accept = re.split(pattern, accept)
accept = [i.split(',') for i in accept if len(i) > 0]
# print(accept)
acceptall = []
print("---")
for i in accept:
    # print(i)

    for j in i:
        acceptall.append(j)
        # print(j)
    
        

# accept.append(j for j in i for i in accept)
print(acceptall)
# [print(i) for i in accept if len(i) > 0]
exit()
accepted_media_types = []
for i in range(0, len(accept), 2):
    [accepted_media_types.append(media) for media in accept[i].split(",")]
    
print(accepted_media_types)
 """

# f = open("/home/rhugaved/", 'rb')
# f = f.read()
# coding = chardet.detect(f).get('encoding')
# print(coding) 


# time = "Sun, 18 Oct 2012 10:36:20 GMT"
# try:
#     last_modified = os.path.getmtime("/home/rhugaved/t.txt")
#     last_modified = datetime.datetime.fromtimestamp(last_modified, datetime.timezone.utc).replace(microsecond=0 ,tzinfo=None)
#     print(last_modified)
#     t = datetime.datetime.strptime(time, "%a, %d %b %Y %X %Z")
#     if t < last_modified:
#         print(t)
# except:
#     print("Invalidc")


# class temp():
#     var = 33
#     def __init__(self):
#         pass
#     def fun(self):
#         self.var = 44
# ob = temp()
# print(ob.var)
# ob.fun()
# print(ob.var)

# logging.basicConfig(level=logging.INFO, )

# s = '''{"Content":"<html><body><h1>Success</h1></body></html>","ContentLength":42,"ContentType":"text/html; charset=utf-8","Elapsed":42,"Headers":"Date: Fri, 23 Oct 2020 13:39:38 GMT\r\nContent-Type: text/html; charset=utf-8\r\nTransfer-Encoding: chunked\r\nConnection: keep-alive\r\nSet-Cookie: __cfduid=daa2879f0b9a583441321ccaf5487efdf1603460377; expires=Sun, 22-Nov-20 13:39:37 GMT; path=/; domain=.reqbin.com; HttpOnly; SameSite=Lax; Secure\r\nCF-Cache-Status: DYNAMIC\r\ncf-request-id: 05f748c5890000e73cbd90d000000001\r\nExpect-CT: max-age=604800, report-uri=\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\"\r\nReport-To: {\"endpoints\":[{\"url\":\"https:\\/\\/a.nel.cloudflare.com\\/report?lkg-colo=11&lkg-time=1603460378\"}],\"group\":\"cf-nel\",\"max_age\":604800}\r\nNEL: {\"report_to\":\"cf-nel\",\"max_age\":604800}\r\nServer: cloudflare\r\nCF-RAY: 5e6bdd827d2de73c-EWR\r\nContent-Encoding: gzip\r\n","Redirects":[],"RedirectsCount":0,"RedirectsTime":0,"StatusCode":"200","StatusDescription":"OK","Success":true,"Timings":{"Connecting":0.00639,"DNS":0.004208,"Receiving":0.00015115737915039062,"Sending":4.76837158203125e-05,"TLS":0.024991,"Total":0.042048,"Waiting":0.016810894012451172},"Version":"1.1"}
# '''
# print(len(s))

# s = '''POST /test HTTP/1.1
# Host: foo.example
# Content-Type: application/x-www-form-urlencoded
# Content-Length: 27

# field1=value1&field2=value2'''

# s = s.splitlines()
# print(s)
# # s.remove('')
# # print(s)

# i = s.index('')
# s.remove('')
# print(s)
# print(i, s[i])

# if len(s) > i:
#     b = s[i:]
#     # for x in b:
#     #     s.remove(x)
    
#     for j in range(len(s)-1, i-1, -1):
#         print(j)
#         s.pop(j)
# print(s)
# print(b)

# exit()
# # s = '''--boundary 
# # Content-Disposition: form-data; name="field1" 

# # value1 
# # --boundary 
# # Content-Disposition: form-data; name="field2"; filename="example.txt" 

# value2
# --boundary--'''
# p = parse_qs(s)
# print(p)

# s = '''--boundary 
# Content-Disposition: form-data; name="field1"

# value1 
# --boundary 
# Content-Disposition: form-data; name="field2"; filename="example.txt"

# value2
# --boundary--'''

# # s= s.replace('"', '')
# # s = s.split('\n')
# # print(len(s))
# # for i in range(0, len(s)-1, 4):
# #     # print(i)
# #     # s[i].replace('"', '')
# #     name = s[i+1].split(' name=')
# #     name = name[1].split('; filename=')
# #     value = s[i+3]
# #     print(name, value)

# d = {'a': '3', 'b':'2'}
# d = parse_qs('fname=Rhugaved&lname=Narmade')
# print(d)
# values_to_write = ';'.join([i[0] for i in d.values()])
# data = values_to_write.encode('utf-8')
# print(values_to_write, data)
# # [print(i) for i in d.values()]

# f = "/home/asdf/asdf.22"
# b = os.path.dirname(f)
# print(b)
# print(b.split('.')[1])

# b = "field1=value1&field2=value2"
# l = b.split('&')
# print(l)
# request_body_dict = [[j for j in i.split('=')] for i in l]
# print(request_body_dict)

# b = ['adsfasdf']


# request_body_string = ""
# for k in b:
#     request_body_string += k + '\n'
# request_body_string =  request_body_string.rstrip().lstrip()
# print(request_body_string)

# s = '''--boundary\r\nContent-Disposition: form-data; name="field1"\r\n\r\nvalue1\r\nvalueaaaaaaa\r\n--boundary\r\nContent-Disposition: form-data; name="field2"; filename="example.txt"\r\nContent-Type: text/plain\r\n\r\nvalue2\r\n--boundary'''

# s = s.split('--boundary\r\n')
# # print(s.splitlines())
# for i in s:
#     if len(i) == 0:
#         #to skip '' which can be a entry as well in the list
#         continue
#     # print(i.lstrip().rstrip())
#     # for the last entry, may contain extra boundary
#     if '--boundary' in i:
#         # print('=====')
#         i = i.replace('\r\n--boundary', '')
    
#     v = i.split('\r\n\r\n')
#     # print(v)
#     # continue
#     value = v[1].lstrip().rstrip()
#     i = v[0]
#     print(i.splitlines())
#     print(value)
#     print('=====')
#     value = v[1]
#     i = v[0]
#     i = i.splitlines()
#     print(i)

# s = '''Content-Disposition: form-data; name="field2"; filename="example.txt"', 'Content-Type: text/plain'''
# pattern = "\"(.*?)\""
# substring = re.findall(pattern, s)
# print(substring)


# s = b'GET\x89 / HTTP/1.1\r\nHost: localhost:8800\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nIf-Modified-Since: Tue, 20 Oct 2020 06:43:15 GMT\r\nCache-Control: max-age=0\r\n\r\n'
# print(s.rstrip())

# print(s.split(b'\r\n\r\n'))
# try:
#     s.decode('utf-8')
#     print(s)
# except:
#     print('Nope')
# body = ''
# image = b''
# # if binary_data:
# for i in s.split(b'\r\n\r\n'):
#     try:
#         body += i.decode('utf-8')
        
#     except:
#         image += i
# print(body)
# print(image)
# s = str(s)
# print(s)
# s = bytearray(s)
# p =''
# for i in s:
#     try:
#         # p += i.decode('utf-8')
#         print(unichr(i))
#         read_next_byte()
#     except:
#         print('bin', i)
#         # p +=i

# print(p)

# with open('request_data_store_temp.txt', 'wb') as f:
#     f.write(s)
#     f.close()

# request_data = ''
# byte_data = b''
# a = ''
# with open('request_data_store_temp.txt', 'rb') as f:
   
#     while f.read(1):
#         # d = f.read(1)
#         f.seek(-1, 1)
#         d = f.read(1)
#         # print(d.decode())
#         try:
            
#             try:
#                 # print('hi')
#                 request_data += d.decode('utf-8')
#                 a += d.decode('utf-8')
#                 if a == '\r\n\r\n':
#                     print('=')
#                     break
#                 elif a in  ['\r\n\r', '\r', '\r\n']:
#                     print('+')
#                     continue

#                 else:
#                     a = ''
#                 # print(d.decode())

#             except:
#                 # print('hello')
#                 byte_data += d
#         except:
#             print('bye')
#             pass

#     print(request_data)
    # print('========')
    # print(byte_data)

# f = open('form_submition_data.json', 'r')
# data = json.load(f)
# l = {'fname': ["Rhugaved"]}
# for d in data:
#     s = all(item in d.items() for item in l.items())
#     if s:
#         print(d)
# s = mimetypes.guess_type('/home/rhugaved/t.py')[0].split('/')[0]
# print(s)


# d = {'a': 3, 'b':4}
# a = '\n'.join((f'{key}, {value}' for (key, value) in d.items()))
# print(a)

# conf_dict = {}
# with open("setup.config", 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line = line.strip()
#         if len(line) > 0:
#             # print(len(line))     
#             # continue       
#             if line[0] == '#':
#                 print(line)
#                 pass
#             else:
#                 try:
#                     l = line.split('=')
#                     print(l)
#                     # continue
#                     l[0] = l[0].strip()
#                     l[1] = l[1].strip()
#                     conf_dict[l[0]] = l[1]
#                 except:   
#                     print("Invalid Sytax in Config file")
#                     conf_dict.clear()
#                     break

# print(conf_dict)


# s= os.stat("/home/rhugaved/TYCourses/CN/Project/SELab").st_mode
# print(stat.S_IRWXU(s)) 
# print(stat.S_IFMT(s))

# s= os.access("/home/rhugaved/TYCourses/CN/Project/SELab/test.txt", os.F_OK)
# print(s)

# def isWritable(name):
#   uid = os.geteuid()
#   gid = os.getegid()
#   s = os.stat(name)
#   mode = s[stat.ST_MODE]
#   return (
#      ((s[stat.ST_UID] == uid) and (mode & stat.S_IWUSR)) or
#      ((s[stat.ST_GID] == gid) and (mode & stat.S_IWGRP)) or
#      (mode & stat.S_IWOTH)
#      )

# print(isWritable("/home/rhugaved/TYCourses/CN/Project/SELab"))

# s = base64.b64encode('rhugaved:rn@123'.encode('utf-8'))
# print(s.decode())

# for i, j, k in os.walk(os.getcwd(), topdown=True):
#     if  'test.txt' in k:
#         print(i)

d = {'a': 3, 'b': 4}
s = 'he'
s += str(d)
print(s)