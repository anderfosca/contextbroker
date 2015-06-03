#!flask/bin/python

__author__ = 'anderson'

import requests, json

getproviders_url = "http://localhost:5000/getProviders"
#for i in range(0, 1000):
 #   r = requests.get(getproviders_url, params={'scope': 'test5', 'entity': ''})
#    print r.json(), r.status_code


entity_id = 'marcos'
entity_type = 'username'
scope_list = 'test2,scope2'
callback_url = 'http://didone.biz'
time = 30

subscribe_url = "http://localhost:5000/subscribe"
subscribe_tuple = {'entity': entity_id, 'type': entity_type, 'scopeList': scope_list, 'callbackUrl': callback_url, 'time': time}
r = requests.get(subscribe_url, params=subscribe_tuple)

getcontext_url = "http://localhost:5000/getContext"
getcontext_tuple = {'scopeList': 'test2', 'entities': 'username|marcos'}
#r = requests.get(getcontext_url, params=getcontext_tuple)

print r.content, r.status_code
