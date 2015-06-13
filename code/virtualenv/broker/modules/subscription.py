__author__ = 'anderson'
import sys
import generic_response
import pymongo
from pymongo import MongoClient
import logging

# subscribe
# dados esperados: parametros URL:
#                               entity - ID da entidade desejada: entity=joao
#                               type - tipo da entidade desejada: type=user
#                               scopeList - lista de scopes desejados, separados por virgula, sem espaco: location,name
#                               callbackUrl - endereco pra onde o Broker vai enviar dados quando atualizados pelo Prov
#                               time - quantidade de tempo de vida da subscription, em minutos, inteiro maior que 0
# descricao: Consumer envia entidade e escopos sobre os quais deseja receber atualizacoes, na sua Url, e um tempo de
#   vida para a subscription
# retorna: mensagem de sucesso ou erro
def subscribe(callback_url, entity_name, entity_type, scope_list, minutes):
    logger = logging.getLogger('broker')
    logger.info('subscription - Initiate - callbackUrl: %s; entity: %s; scope_list: %s; minutes: %s',
                callback_url, entity_type+'|'+entity_name, scope_list, minutes)
    try:
        # TODO validar os campos, url ser URL, entidade e escopo(s) existirem de fato
        ######################MONGODB
        client = MongoClient()
        db = client.broker
        scopes_ids = []
        for result in db.scopes.find({'name': {'$in': scope_list.split(',')}}, {'_id': 1}):
            scopes_ids.append(result["_id"])
        entity_el = db.entities.find_one({'name': entity_name, 'type': entity_type}, {'_id': 1})
        if entity_el and len(scopes_ids) > 0:
            db.subscriptions.insert_one({'callback_url': callback_url, 'minutes': minutes,
                                         'entity_id': entity_el["_id"], 'scopes': scopes_ids})
            return generic_response.generate_response('OK','200','Subscription Success',
                                                      'subscription','','',entity_name,entity_type,scope_list)
        else:
            logger.warn('subscription - Bad Parameters - callbackUrl: %s; entity: %s; scope_list: %s; minutes: %s')
            return generic_response.generate_response('ERROR','400','Bad Parameters',
                                                      'subscription','','',entity_name,entity_type,scope_list)
        #####################MONGODB

    except Exception as e:
        logger.warn('subscription - Internal Error: %s', sys.exc_info()[0])
        error_message = "Internal Error"
        return generic_response.generate_response('ERROR','500',error_message,
                                                  'subscription','','','','','')


