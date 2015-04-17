__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb

tree = ET.parse('xmls/adv2.xml')
root = tree.getroot()
for adv in root.find('ctxAdvs').findall('ctxAdv'):
    id = adv.find('contextProvider').get('id')
    urlRoot = adv.find('urlRoot').text
    lat, lon, location = '', '', ''
    if adv.find('providerLocation') is not None:
        lat = adv.find('providerLocation').find('lat').text
        lon = adv.find('providerLocation').find('lon').text
        location = adv.find('providerLocation').find('location').text
    for scope in adv.find('scopes').findall('scopeDef'):
        urlPath = scope.find('urlPath').text
        entityTypes = scope.find('entityTypes').text
        for inputEl in scope.find('inputDef').findall('inputEl'):
            name = inputEl.get('name')
            type = inputEl.get('type')
            print id, urlRoot, lat, lon, location, urlPath, entityTypes, name, type





#con = MySQLdb.connect(host='localhost', user='root', passwd='showtime',db='test')
#c = con.cursor()
#for i in xrange(5):
#    c.execute("INSERT INTO t1 VALUES (%i, 'numero%s')"%(i, i))

#con.commit()
