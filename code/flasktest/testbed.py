__author__ = 'anderson'
import xml.etree.ElementTree as ET

with open ("filename.xml", "r") as myfile:
    data=myfile.read()

root = ET.fromstring(data)

print root