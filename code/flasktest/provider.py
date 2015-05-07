#!flask/bin/python

__author__ = 'anderson'

import requests, json
import xml.etree.ElementTree as ET


class Provider(object):

    def __init__(self, name, version, url, lat, lon, location_description, scopes):
        self.name = name
        self.version = version
        self.url = url
        self.lat = lat
        self.lon = lon
        self.location_description = location_description
        self.scopes = scopes  # list of dictionaries

    def generate_xml(self):
        root = ET.Element("contextML")
        ctxAdvs = ET.SubElement(root, "ctxAdvs")
        ctxAdv = ET.SubElement(ctxAdvs, "ctxAdv")
        ET.SubElement(ctxAdv, "contextProvider", id=self.name, v=self.version)
        ET.SubElement(ctxAdv, "urlRoot").text = self.url
        providerLocation = ET.SubElement(ctxAdv, "providerLocation")
        if len(self.lat) > 0:
            ET.SubElement(providerLocation, "lat").text = self.lat
            ET.SubElement(providerLocation, "lon").text = self.lon
        if len(self.location_description) > 0:
            ET.SubElement(providerLocation, "location").text = self.location_description

        if len(self.scopes) > 0:
            scopesTag = ET.SubElement(ctxAdv, "scopes")
            for scope in self.scopes:
                print scope
                scopeDef = ET.SubElement(scopesTag, "scopeDef", n=scope['name'])
                ET.SubElement(scopeDef, "urlPath").text = scope['url']
                ET.SubElement(scopeDef, "entityTypes").text = scope['entityTypes']
                inputDef = ET.SubElement(scopeDef, "inputDef")
                for input in scope['inputs']:
                    ET.SubElement(inputDef, "inputEl", name=input['name'], type=input['type'])

        return ET.tostring(root)

    def advertise(self, broker_url):
        xml_string = self.generate_xml()
        target_url = broker_url+"/advertisement"
        #dataA = json.dumps({'advMessage': advMessage})
        r = requests.post(target_url, xml_string)
        print r.json(), r.status_code


provider_scopes = [
    {'name': "scope1",
     'url': "/scope1",
     'entityTypes': "username,mobile",
     'inputs': [
         {'name': "lat",
          'type': "position:latitude"},
         {'name': "lon",
          'type': "position:longitude"}
     ]},
    {'name': "scope2",
     'url': "/scope2",
     'entityTypes': "username,mobile",
     'inputs': [
         {'name': "lat",
          'type': "position:latitude"},
         {'name': "lon",
          'type': "position:longitude"}
     ]}
]

provider = Provider("provTeste", "1.0.0", "http://provTeste", "0", "0", "aqui", provider_scopes)
# with open ("filename.xml", "r") as myfile:
#     advMessage=myfile.read().replace("\n",'')
provider.advertise("http://localhost:5000")

