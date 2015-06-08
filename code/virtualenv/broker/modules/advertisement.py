__author__ = 'anderson'

import xml.etree.ElementTree as ET
import re
import sys
import generic_response
import pymongo
from pymongo import MongoClient

# register_provider
# dados esperados: xml com informacoes do Provider
# descricao: Faz o registro (ou atualizacao) das informacoes do Provider que enviou
# os dados
# retorna: mensagem de sucesso ou erro
# TODO checar comportamento de conexao com o MySQL, con, cursor, close(), etc
def register_provider(broker_info):
    broker_info = re.sub(' xmlns="[^"]+"', '', broker_info, count=1)
    broker_info = re.sub(' xmlns:xsi="[^"]+"', '', broker_info, count=1)
    broker_info = re.sub(' xsi:schemaLocation="[^"]+"', '', broker_info, count=1)

    root = ET.fromstring(broker_info)
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
        provider = {'name': nameProv, 'version': version, 'url': urlRoot,
                    'location': lat+';'+lon, 'location_desc': location}
        client = MongoClient()
        db = client.broker
        providers_collection = db.providers
        provider_el_id = providers_collection.insert_one(provider).inserted_id
###########################MONGODB
    except Exception as e:
        error_message = "Erro no registro do Provider: %s" % (sys.exc_info()[0])
        return generic_response.generate_response('ERROR','400',error_message,'advertisement',nameProv,version,'','','')
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
            scope_element = {'name': name_scope, 'url_path': url_path,
                             'entity_types': entity_types, 'inputs': inputs, 'provider_id': provider_el_id}
            scopes_collection = db.scopes
            scopes_collection.insert_one(scope_element)
###########################MONGODB
        except Exception as e:
            error_message = "Erro no registro do Scope: %s" % (sys.exc_info()[0])
            return generic_response.generate_response('ERROR','500',error_message,
                                                  'getProviders','','','','','')

    return generic_response.generate_response('OK','200','Advertisement succeeded','advertisement',nameProv,version,'','','')

