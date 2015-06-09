__author__ = 'anderson'

import xml.etree.ElementTree as ET
import sys
import generic_response
import logging
import pymongo
from pymongo import MongoClient

# get_providers
# quem acessa: Consumer
# dados esperados: scope e entity_type(opcional)
# descricao: Consumer faz uma requisicao dos Providers cadastrados no Broker que satisfacam scope e entity_type pedidos
# retorna: xml com ctxPrvEl, com o scope e os Providers que possuem esse scope
# cadastrados
def get_providers(scope, entity_type):
    logger = logging.getLogger('broker')
    logger.info('get_providers - Initiate - Scope: %s; EntityType: %s', scope, entity_type)
    if len(scope) == 0:
        logger.warn('get_providers - No Scope provided')
        return generic_response.generate_response('ERROR','400','Bad Parameter',
                                                  'getProviders','','','',entity_type,scope)
    try:    # aqui eh feita a insercao do provider no banco
        ########################MONGODB
        client = MongoClient()
        db = client.broker
        provider_ids = []
        for r in db.scopes.find({'name': scope}, {'provider_id': 1}):
            provider_ids.append(r['provider_id'])
        providers = db.providers.find({'_id': {'$in': provider_ids}})
        ########################MONGODB
        if providers.count() == 0:  # Retorna erro, nao achou nenhum Provider que satisfaz a requisicao
            logger.warn('get_providers - No Providers for Scope: %s', scope)
            return generic_response.generate_response('ERROR','400','No results found',
                                                      'getProviders','','','',entity_type,scope)
        root = ET.Element("contextML")  # Inicio da construcao do XML
        ctxPrvEls = ET.SubElement(root, "ctxPrvEls")
        ctxPrvEl = ET.SubElement(ctxPrvEls, "ctxPrvEl")
        par_scope = ET.SubElement(ctxPrvEl, "par", n="scope")
        par_scope.text = scope
        par_Aproviders = ET.SubElement(ctxPrvEl, "parA", n="contextProviders")

        if len(entity_type) == 0:  # Caso soh o scope tenha sido definido
            for provider in providers:
                par_Sproviders = ET.SubElement(par_Aproviders, "parS", n="contextProvider")
                ET.SubElement(par_Sproviders, "par", n="id").text = provider['name']
                ET.SubElement(par_Sproviders, "par", n="url").text = provider['url']
        else:
            found = False  # variavel local, para caso nao achar nenhum com a entidade desejada
            for provider in providers:
                if entity_type in provider['entity_types'].split(','):  # provider[2] contem as entidades, separadas por ,
                    found = True  # achou ao menos um
                    par_Sproviders = ET.SubElement(par_Aproviders, "parS", n="contextProvider")
                    ET.SubElement(par_Sproviders, "par", n="id").text = provider['name']
                    ET.SubElement(par_Sproviders, "par", n="url").text = provider['url']
            if not found:
                logger.warn('get_providers - No Results Found for Scope: %s; EntityType: %s', scope, entity_type)
                return generic_response.generate_response('ERROR','400','No results found',
                                                          'getProviders','','','',entity_type,scope)
        logger.info('get_providers - Success - Scope: %s; EntityType: %s', scope, entity_type)
        return ET.tostring(root)  # Arvore xml resultante transformada numa str
    except Exception as e:
        logger.error('get_providers - Internal Error: %s; Scope: %s; EntityType: %s',
                     sys.exc_info()[0], scope, entity_type)
        error_message = "Internal Error"
        return generic_response.generate_response('ERROR','500',error_message,
                                                  'getProviders','','','',entity_type,scope)

