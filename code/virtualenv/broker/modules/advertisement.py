__author__ = 'anderson'

import xml.etree.ElementTree as ET
import re
import sys
import generic_response
import pymongo
from pymongo import MongoClient
import logging

# register_provider
# dados esperados: xml com informacoes do Provider
# descricao: Faz o registro (ou atualizacao) das informacoes do Provider que enviou
# os dados
# retorna: mensagem de sucesso ou erro
# TODO checar comportamento de conexao com o MySQL, con, cursor, close(), etc
def register_provider(xml_string):
    logger = logging.getLogger('broker')
    logger.info('advertisement - Initiating')

    xml_string = re.sub(' xmlns="[^"]+"', '', xml_string, count=1)
    xml_string = re.sub(' xmlns:xsi="[^"]+"', '', xml_string, count=1)
    xml_string = re.sub(' xsi:schemaLocation="[^"]+"', '', xml_string, count=1)

    root = ET.fromstring(xml_string)
    adv = root.find('ctxAdvs').find('ctxAdv')
    nameProv = adv.find('contextProvider').get('id')
    version = adv.find('contextProvider').get('v')
    urlRoot = adv.find('urlRoot').text
    lat, lon, location = '', '', ''
    if adv.find('providerLocation') is not None:    # Location pode nao ter sido anunciada
        lat = adv.find('providerLocation').find('lat').text
        lon = adv.find('providerLocation').find('lon').text
        location = adv.find('providerLocation').find('location').text
    try:    # aqui eh feita a insercao do provider no banco
###########################MONGODB
        logger.info('advertisement - Registering Provider: %s %s', nameProv, urlRoot)
        client = MongoClient()
        db = client.broker
        on_insert = {'name': nameProv, 'url': urlRoot}
        on_update = {'version': version, 'location': lat+';'+lon, 'location_desc': location}
        if db.providers.update_one(on_insert, {'$setOnInsert': on_insert, '$set': on_update}, upsert=True).upserted_id:
            logger.info('advertisement - Registered Provider: %s %s', nameProv, urlRoot)
        else:
            logger.info('advertisement - Updated Provider: %s %s', nameProv, urlRoot)
        provider_el = db.providers.find_one({'name': nameProv, 'url': urlRoot})
###########################MONGODB
    except Exception as e:
        logger.error('advertisement - Internal Error on Registering Provider: %s %s: %s',
                     nameProv, urlRoot,sys.exc_info()[0])
        error_message = "Internal Error"
        return generic_response.generate_response('ERROR','400',error_message,
                                                  'advertisement',nameProv,version,'','','')
    # a partir daqui sao inseridos os scopes, na tabela de scopes
    for scope in adv.find('scopes').findall('scopeDef'):
        name_scope = scope.get('n')
        url_path = urlRoot + scope.find('urlPath').text
        entity_types = scope.find('entityTypes').text
        inputs = []
        for inputEl in scope.find('inputDef').findall('inputEl'):   # inputs sao colocados juntos em string
            input_name = inputEl.get('name')
            input_type = inputEl.get('type')
            inputs.append(input_name+";"+input_type)
        try:
###########################MONGODB
            logger.info('advertisement - Inserting Scope: %s %s', name_scope, url_path)
            on_insert = {'name': name_scope, 'url_path': url_path, 'provider_id': provider_el['_id']}
            on_update = {'entity_types': entity_types, 'inputs': inputs}
            if db.scopes.update_one(on_insert, {'$setOnInsert': on_insert, '$set': on_update}, upsert=True).upserted_id:
                logger.info('advertisement - Inserted Scope: %s %s, From Provider: %s',
                            name_scope, url_path, provider_el['name'])
            else:
                logger.info('advertisement - Updated Scope: %s %s, From Provider: %s',
                            name_scope, url_path, provider_el['name'])
###########################MONGODB
        except Exception as e:
            logger.error('advertisement - Internal Error on Registering Scope: %s %s: %s',
                         name_scope, url_path, sys.exc_info()[0])
            error_message = "Internal Error"
            return generic_response.generate_response('ERROR','500',error_message,
                                                  'getProviders','','','','','')

    return generic_response.generate_response('OK','200','Advertisement Success',
                                              'advertisement',nameProv,version,'','','')