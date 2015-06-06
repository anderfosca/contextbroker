__author__ = 'anderson'

import sys
import MySQLdb
import xml.etree.ElementTree as ET
import config
import generic_response


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
    found=False
    for scopeName in scope_list.split(','):
        try:
            con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
            for entity in entities.split(','):
                c = con.cursor()
                c.execute("SELECT rt.provider_id, rt.timestamp, rt.expires, rt.dataPart, pr.name, pr.version"
                          " FROM registryTable rt, providers pr, entities, scopes "
                          "WHERE rt.scope_id=scopes.scope_id AND rt.entity_id=entities.entity_id "
                          "AND entities.name= '%s' AND entities.type='%s' AND scopes.name='%s'" %
                                            (entity.split('|')[1], entity.split('|')[0], scopeName))
                elements = c.fetchone()
                c.close()
                if  elements is not None:
                    found=True
                    ctxEl = ET.SubElement(ctxEls, "ctxEl")
                    ET.SubElement(ctxEl, "contextProvider", id=elements[4], v=elements[5])
                    ET.SubElement(ctxEl, "entity", id=entity.split('|')[0], type=entity.split('|')[1])
                    ET.SubElement(ctxEl, "scope").text = scopeName
                    ET.SubElement(ctxEl, "timestamp").text = elements[1]
                    ET.SubElement(ctxEl, "expires").text = elements[2]
                    ET.SubElement(ctxEl, "dataPart").text = elements[3]
        except MySQLdb.Error, e:
            c.close()
            con.commit()
            con.close()
            error_message = "<p>Erro no GetContext %s: %s</p>" % (e.args[0], e.args[1])
            return error_message
    if found:
        xml_string = ET.tostring(root).replace('&lt;', '<').replace('&gt;', '>').replace('\n', '')
    else:
        xml_string = generic_response.generate_response('ERROR','400','Nothing found','getContext','','','','','')
    return xml_string