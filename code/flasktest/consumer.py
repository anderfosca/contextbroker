#!flask/bin/python

__author__ = 'anderson'

import requests, json

target_url = "http://localhost:5000/getProviders"
r = requests.get(target_url)

print r.json(), r.status_code

