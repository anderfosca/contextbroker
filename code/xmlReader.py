__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb

tree = ET.parse('teste.xml')
root = tree.getroot()



con = MySQLdb.connect(host='localhost', user='root', passwd='showtime',db='teste')
c = con.cursor()
for i in xrange(5):
    c.execute("INSERT INTO t1 VALUES ('numero%s', %i)"%(i, i))

con.commit()
