#!flask/bin/python

__author__ = 'anderson'

import requests, json

with open ("filename.xml", "r") as myfile:
    advMessage=myfile.read().replace("\n",'')

target_url = "http://localhost:5000/advertisement"
dataA = json.dumps({'advMessage': advMessage})
r = requests.post(target_url, advMessage)

print r.json(), r.status_code

