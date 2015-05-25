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

    def generate_advertise_xml(self):
        NS_XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
        root = ET.Element("contextML", xmlns="http://ContextML/1.6c")
        root.set(NS_XSI + "schemaLocation", "http://ContextML/1.7http://cark3.cselt.it/schemas/ContextML-1.6.c.xsd")
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

    def generate_update_xml(self):
        with open('upd1.xml', 'r') as f:
            xmlstring= f.read()
        return xmlstring


    def advertise(self, broker_url):
        xml_string = self.generate_advertise_xml()
        print xml_string
        target_url = broker_url+"/advertisement"
        #dataA = json.dumps({'advMessage': advMessage})
        r = requests.post(target_url, xml_string)
        print r.json(), r.status_code


    def update(self, broker_url):
        xml_string = self.generate_update_xml()
        print xml_string

        target_url = broker_url+"/update"
        #dataA = json.dumps({'advMessage': advMessage})
        r = requests.post(target_url, xml_string)
        print r.json(), r.status_code


provider_scopes = [
    {'name': "test8",
     'url': "/test8",
     'entityTypes': "username,mobile",
     'inputs': [
         {'name': "lat",
          'type': "position:latitude"},
         {'name': "lon",
          'type': "position:longitude"}
     ]},
    {'name': "scope8",
     'url': "/scope8",
     'entityTypes': "username,mobile",
     'inputs': [
         {'name': "lat",
          'type': "position:latitude"},
         {'name': "lon",
          'type': "position:longitude"}
     ]}
]

provider = Provider("provTeste9", "1.0.0", "http://provTeste9", "0", "0", "aqui", provider_scopes)
# with open ("filename.xml", "r") as myfile:
#     advMessage=myfile.read().replace("\n",'')
provider.advertise("http://localhost:5000")

#provider.update("http://localhost:5000")

