import json
import sys
import os
import requests
from requests import Request, Session
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)

# API Version
version = 0.1

class APIError(Exception):
    pass

def print_fatal(error):
    print('Error! {0}'.format(error))
    raise APIError('FUN3D API Error')

try:
    with open(os.path.expanduser('~/.simulation/simulation.key'),'r') as f:
        k = f.read().strip().split(':')
        user_id = k[0]
        username = k[1]
        email = k[2]
        key = k[3]
except Exception as e:
    print_fatal('Could not read ~/.simulation/simulation.key')

auth = {'email' : email,'user_id' : user_id, 'version' : version}
headers = {'Cookie' : 'email=' + email + '; key=' + key}

s = Session()

def auth_request(target):
    domain = 'https://simulation.cloud'
    req = Request('GET','{0}/highthroughput/auth/{1}'.format(domain,target),
                  data=auth,headers=headers)
    prepped = s.prepare_request(req)
    return s.send(prepped,timeout=30)

try:
    ip = auth_request('ip').text
    print('REMINDER. To login to your server, type:')
    print('ssh -i ~/.simulation/simulation {0}@{1}'.format(username,ip))

except Exception as e:
    print_fatal('Could not retrieve ip address from server.')

try:
    cert = auth_request('cert').json().get('cert')
except Exception as e:
    print_fatal('Could not retrieve SSL certificate from server.')

try:
    if cert is not None:
        certpath = os.path.expanduser('~/.simulation/certificate.pem')
        with open(certpath,'w') as f:
            f.write(cert)
        verify = certpath
    else:
        verify = True

except OSError as e:
    print_fatal(str(e))




def process(response):
    if response.status_code != requests.codes.ok:
        raise APIError(response.text)
    try:
        js = response.json()
        print('Have json')
        print(js)
    except Exception as e:
        return response

    error = None
    try:
        error = js.get('ServerError')
    except Exception as e:
        pass
    if error is not None:
        raise APIError(error)
    return js

def put_file(origin, destination):
    sftp.put(origin,destination)

def put_dir(destination):
    sftp.mkdir(destination)

def upload_dir(url,directory):
    for item in os.listdir(directory):
        newurl = url + '/' + item
        newitem = os.path.join(directory,item)
        if os.path.isfile(newitem):
            post(newurl,{},filename=newitem)
        else:
            upload_dir(newurl,newitem)


def request(target,data,request_type,files=None):
    s = Session()
    #url = 'http://simulation.cloud:8080{0}?url={1}'.format(target,ip)
    url = 'https://{0}:8080{1}'.format(ip,target)
    #url = 'https://simulation.cloud:8080{0}?url={1}&userid={2}'.format(target,ip,user_id)
    req = Request(request_type, url, data=data, headers=headers,files=files)
    prepped = s.prepare_request(req)
    resp = s.send(prepped,timeout=30,verify=verify)
    return resp

def post(target,data={},filename=None):
    files = None
    if filename is not None:
        data = open(filename,'rb')
    return process(request(target,data,'POST',files))

def put(target,data={}):
    return process(request(target,data,'PUT'))

def get(target,data={}):
    return process(request(target,data,'GET'))

def delete(target,data={}):
    return process(request(target,data,'DELETE'))
