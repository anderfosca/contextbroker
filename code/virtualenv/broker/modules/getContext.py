__author__ = 'anderson'

import sys
import MySQLdb
import xml.etree.ElementTree as ET
import generic_response
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

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
            for entity in entities.split(','):
                #################MONGODB
                entity_type, entity_name = entity.split('|')
                client = MongoClient()
                db = client.broker
                entity_el = db.entities.find_one({'name': entity_name, 'type': entity_type})
                scope_el = db.scopes.find_one({'name': scopeName})
                if entity_el and scope_el:
                    registry = db.registries.find_one({'entity._id': entity_el["_id"], 'scope._id': scope_el["_id"]})
                #################MONGODB
                    if registry is not None:
                        found=True
                        ctxEl = ET.SubElement(ctxEls, "ctxEl")
                        ET.SubElement(ctxEl, "contextProvider", id=registry['provider']['name'], v=registry['provider']['version'])
                        ET.SubElement(ctxEl, "entity", id=entity.split('|')[0], type=entity.split('|')[1])
                        ET.SubElement(ctxEl, "scope").text = scopeName
                        ET.SubElement(ctxEl, "timestamp").text = registry['timestamp']
                        ET.SubElement(ctxEl, "expires").text = registry['expires']
                        ET.SubElement(ctxEl, "dataPart").text = registry['data_part']
        except Exception as e:
            error_message = "Erro no GetContext: %s" % (sys.exc_info()[0])
            return generic_response.generate_response('ERROR','400',error_message,'getContext','','','','','')
    if found:
        xml_string = ET.tostring(root).replace('&lt;', '<').replace('&gt;', '>').replace('\n', '')
    else:
        xml_string = generic_response.generate_response('ERROR','400','Nothing found','getContext','','','','','')
    return xml_string