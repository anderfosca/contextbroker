__author__ = 'anderson'

import xml.etree.ElementTree as ET
import sys
import re
import generic_response
import pymongo
from pymongo import MongoClient

def send_to_consumer(url, xml_string):
    print "sending to: " + url + '\n' + xml_string
    #r = requests.post(url, xml_string)
    #print r.json(), r.status_code

# context_update
# dados esperados: xml com informacoes do update do Provider
# descricao: Registra os dados fornecidos pelo Provider na tabela de registros (registryTable)
# retorna: mensagem de sucesso ou erro
# TODO verificar consistencia dos dados
# TODO verificar erros possiveis
def context_update(xml_string_original):
    """

    :rtype : str
    """
    xml_string = re.sub(' xmlns="[^"]+"', '', xml_string_original, count=1)
    xml_string = re.sub(' xmlns:xsi="[^"]+"', '', xml_string, count=1)
    xml_string = re.sub(' xsi:schemaLocation="[^"]+"', '', xml_string, count=1)
    root = ET.fromstring(xml_string)

    for ctxEl in root.find('ctxEls').findall('ctxEl'):
        nameProv = ctxEl.find('contextProvider').get('id')
        version = ctxEl.find('contextProvider').get('v')
        entityType = ctxEl.find('entity').get('type')
        entityId = ctxEl.find('entity').get('id')
        scope = ctxEl.find('scope').text
        timestamp = ctxEl.find('timestamp').text
        expires = ctxEl.find('expires').text
        parList=[]
        for par in list(ctxEl.find('dataPart')):
            parList.append(ET.tostring(par))
        dataPart = "".join(parList)
        try:
            ###################################MONGODB
            client = MongoClient()
            db = client.broker
            provider_el = db.providers.find_one({'name': nameProv})
            scope_el = db.scopes.find_one({'name': scope, 'provider_id': provider_el['_id']})
            ##################################MONGODB
            #########################MONGODB
            entity_element = {'name': entityId, 'type': entityType}
            db.entities.update_one(entity_element, {'$setOnInsert': entity_element}, upsert=True)
            entity_el = db.entities.find_one(entity_element)
            #########################MONGODB
#################################MONGODB
            on_insert = {'provider': provider_el, 'scope': scope_el, 'entity': entity_el}
            on_update = {'timestamp': timestamp, 'expires': expires, 'data_part': dataPart}
            db.registries.update_one(on_insert, {'$setOnInsert': on_insert, '$set': on_update}, upsert=True)
################################MONGODB

            # hora de conferir as subscriptions
            results = check_subscriptions(entityId, entityType, scope)
            if results.count() > 0:
                for result in results:
                    send_to_consumer(result['callback_url'], xml_string_original)
                return generic_response.generate_response('OK','200','Update and subscription success','update',nameProv,version,entityId,entityType,scope)
            else:
                return generic_response.generate_response('OK','200','Update success','update',nameProv,version,entityId,entityType,scope)
        except Exception as e:
            error_message = "Erro no registro do Update: %s" % (sys.exc_info()[0])
            return generic_response.generate_response('ERROR','500',error_message,'update',nameProv,version,entityId,entityType,scope)

# check_subscriptions
# dados esperados: entity, scope
# descricao: Consumer envia entidade e escopos sobre os quais deseja receber atualizacoes, na sua Url, e um tempo de
#   vida para a subscription
# # retorna: mensagem de sucesso ou erro
def check_subscriptions(entity_name, entity_type, scope):
    """

    :rtype : str
    :returns :
    """
    #################################MONGODB
    client = MongoClient()
    db = client.broker
    entity_el_id = db.entities.find_one({'name': entity_name, 'type': entity_type}, {'_id': 1})["_id"]
    scope_el_id = db.scopes.find_one({'name': scope}, {'_id': 1})["_id"]
    results = db.subscriptions.find({'entity_id': entity_el_id,
                                    'scopes': {'$in': [scope_el_id]}}, {'callback_url': 1})
    ################################MONGODB
    for r in results:
        print r['callback_url']

    return results
