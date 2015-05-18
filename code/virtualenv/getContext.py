__author__ = 'anderson'

import sys
import MySQLdb
import xml.etree.ElementTree as ET


# getContext
# dados esperados: scopeList - lista de scopes, separados por virgula, sem espacos, nao pode ser vazio
#                  entities - lista de IDs e tipos, separados pro virgula, sem espaco:
#                                                                           entities=user|joao,user|roberto,...
# descricao: procura na tabela de registros o ultimo registro que corresponde aos parametros dados
# retorna: ctxEL mensagem, com os dados que combinem com os parametros, ou uma mensagem de erro
def get_context(scope_list, entities):
    NS_XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
    root = ET.Element("contextML", xmlns="http://ContextML/1.6c")
    root.set(NS_XSI + "schemaLocation", "http://ContextML/1.7http://cark3.cselt.it/schemas/ContextML-1.6.c.xsd")
    ctxEls = ET.SubElement(root, "ctxEls")
    for scopeName in scope_list.split(','):
        try:
            con = MySQLdb.connect(host='localhost', user='broker_manager', passwd='senhamanager', db='broker')
            c = con.cursor()
            c.execute("SELECT scope_id FROM scopes WHERE name = '%s'" % scopeName)
            scope_id = c.fetchone()[0]
            c.close()
            for entity in entities.split(','):
                print scope_id, entity
                c = con.cursor()
                c.execute("SELECT provider_id, timestamp, expires, dataPart FROM registryTable "
                          "WHERE scope_id = '%s' AND entity = '%s'" % (scope_id, entity))
                elements = c.fetchone()
                c.close()
                c = con.cursor()
                c.execute("SELECT name, version FROM providers "
                          "WHERE provider_id = '%s'" % elements[0])
                provider_elements = c.fetchone()
                c.close()
                ctxEl = ET.SubElement(ctxEls, "ctxEl")
                ET.SubElement(ctxEl, "contextProvider", id=provider_elements[0], v=provider_elements[1])
                ET.SubElement(ctxEl, "entity", id=entity.split('|')[0], type=entity.split('|')[1])
                ET.SubElement(ctxEl, "scope").text = scopeName
                ET.SubElement(ctxEl, "timestamp").text = elements[1]
                ET.SubElement(ctxEl, "expires").text = elements[2]
                ET.SubElement(ctxEl, "dataPart").text = elements[3]
                print elements[3]
        except MySQLdb.Error, e:
            c.close()
            con.commit()
            con.close()
            error_message = "<p>Erro no GetContext %s: %s</p>" % (e.args[0], e.args[1])
            return error_message
    return ET.tostring(root).replace('&lt;', '<').replace('&gt;', '>').replace('\n', '')
