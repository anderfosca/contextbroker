__author__ = 'anderson'

import sys
import requests
import xml.etree.ElementTree as ET
import generic_response
import pymongo
from pymongo import MongoClient
import logging
# getContext
# dados esperados: scopeList - lista de scopes, separados por virgula, sem espacos, nao pode ser vazio
#                  entities - lista de IDs e tipos, separados pro virgula, sem espaco:
#                                                                           entities=user|joao,user|roberto,...
# descricao: procura na tabela de registros o ultimo registro que corresponde aos parametros dados
# retorna: ctxEL mensagem, com os dados que combinem com os parametros, ou uma mensagem de erro
def get_context(scope_list, entities):
    logger = logging.getLogger('broker')
    logger.info('getContext - Initiate')

    NS_XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
    root = ET.Element("contextML", xmlns="http://ContextML/1.6c")
    root.set(NS_XSI + "schemaLocation", "http://ContextML/1.7http://cark3.cselt.it/schemas/ContextML-1.6.c.xsd")
    ctxEls = ET.SubElement(root, "ctxEls")
    found = False
    for scopeName in scope_list.split(','):
        for entity in entities.split(','):
            try:
                #################MONGODB
                entity_type, entity_name = entity.split('|')
                logger.info('getContext - Searching registries for scope: %s, entity: %s', scopeName, entity)
                client = MongoClient()
                db = client.broker
                entity_el = db.entities.find_one({'name': entity_name, 'type': entity_type})
                scope_el = db.scopes.find_one({'name': scopeName})
                if entity_el and scope_el:
                    registry = db.registries.find_one({'entity._id': entity_el["_id"], 'scope._id': scope_el["_id"]})
                #################MONGODB
                    if registry is not None:
                        logger.info('getContext - Found one registry for %s %s', scopeName, entity)
                        found=True
                        ctxEl = ET.SubElement(ctxEls, "ctxEl")
                        ET.SubElement(ctxEl, "contextProvider", id=registry['provider']['name'], v=registry['provider']['version'])
                        ET.SubElement(ctxEl, "entity", id=entity.split('|')[0], type=entity.split('|')[1])
                        ET.SubElement(ctxEl, "scope").text = scopeName
                        ET.SubElement(ctxEl, "timestamp").text = registry['timestamp']
                        ET.SubElement(ctxEl, "expires").text = registry['expires']
                        ET.SubElement(ctxEl, "dataPart").text = registry['data_part']
            except Exception as e:
                logger.error('getContext - Internal Error: %s %s: %s', scopeName, entity, sys.exc_info()[0])
                error_message = "Internal Error"
                return generic_response.generate_response('ERROR','400',error_message,'getContext','','','','','')
    if found:
        logger.info('getContext - Success')
        return ET.tostring(root).replace('&lt;', '<').replace('&gt;', '>').replace('\n', '')
    else:
        logger.warn('getContext - No results found. Sending getContext message to related Providers')
        response = ''
        for scopeName in scope_list.split(','):
                client = MongoClient()
                db = client.broker
                scope_els = db.scopes.find({'name': scopeName}, {'provider_id': 1})
                for scope in scope_els:
                    provider_el = db.providers.find_one({'_id': scope['provider_id']}, {'url': 1})
                    getcontext_url = provider_el['url'] + "/getContext"
                    getcontext_tuple = {'scopeList': scopeName, 'entities': entities}
                    logger.info('getContext - Sending getContext message to Provider %s, scope: %s; entities: %s',
                                getcontext_url, scopeName, entities)
                    try:
                        r = requests.get(getcontext_url, params=getcontext_tuple).content
                        logger.warn('getContext - Received response from Provider %s', getcontext_url)
                    except requests.ConnectionError:
                        logger.warn('getContext - Connection failed with Provider %s', getcontext_url)
                        r=''
                        pass
                    finally:
                        response = response + r
        return response
