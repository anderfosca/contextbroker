__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import ast
import sys


# get_providers
# quem acessa: Consumer
# dados esperados: nenhum
# descricao: Consumer faz uma requisicao dos Providers cadastrados no Broker
# retorna: xml com estrutura de Advertisement, contendo as informacoes dos Providers
# cadastrados
def get_providers():
    # criacao da arvore xml
    root = ET.Element("contextML")
    ctxAdvs = ET.SubElement(root, "ctxAdvs")

    con = MySQLdb.connect(host='localhost', user='root', passwd='showtime', db='broker')
    cursor = con.cursor()
    # select de todos os Providers cadastrados no Broker
    sql = "SELECT provider_id, name, url, version, location, location_desc FROM providers"

    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()

    for provider in results:
        ctxAdv = ET.SubElement(ctxAdvs, "ctxAdv")
        ET.SubElement(ctxAdv, "contextProvider", id=provider[1], v=provider[3])
        ET.SubElement(ctxAdv, "urlRoot").text = provider[2]
        if len(provider[4]) > 1:
            providerLocation = ET.SubElement(ctxAdv, "providerLocation")
            ET.SubElement(providerLocation, "lat").text = provider[4].split(';')[0]
            ET.SubElement(providerLocation, "lon").text = provider[4].split(';')[1]
            ET.SubElement(providerLocation, "location").text = provider[5]
        # seleciona os scopes relacionados a este provider
        sql = "SELECT name, urlPath, entityTypes, inputs FROM scopes WHERE provider_id = %s" % (provider[0])
        cursor = con.cursor()
        cursor.execute(sql)
        scopeResults = cursor.fetchall()
        cursor.close()
        if len(scopeResults) > 0:   # montagem dos scopes no xml
            scopes = ET.SubElement(ctxAdv, "scopes")
            for scope in scopeResults:
                scopeDef = ET.SubElement(scopes, "scopeDef", n=scope[0])
                ET.SubElement(scopeDef, "urlPath").text = scope[1]
                ET.SubElement(scopeDef, "entityTypes").text = scope[2]
                inputDef = ET.SubElement(scopeDef, "inputDef")
                inputList = ast.literal_eval(scope[3])
                for input in inputList:
                    ET.SubElement(inputDef, "inputEl", name=input.split(';')[0], type=input.split(';')[1])

    con.commit()
    con.close()
    xmlString = ET.tostring(root)   # arvore xml resultante transformada numa string
    return xmlString