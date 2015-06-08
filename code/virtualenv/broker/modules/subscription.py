__author__ = 'anderson'
import sys
import generic_response
import pymongo
from pymongo import MongoClient

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
    try:
        # TODO validar os campos, url ser URL, entidade e escopo(s) existirem de fato
        ######################MONGODB
        client = MongoClient()
        db = client.broker
        scopes_ids = []
        for result in db.scopes.find({'name': {'$in' : scope_list.split(',')}}, {'_id': 1}):
            scopes_ids.append(result["_id"])
        entity_el = db.entities.find_one({'name': entity_name, 'type': entity_type}, {'_id': 1})
        if entity_el and len(scopes_ids) > 0:
            db.subscriptions.insert_one({'callback_url': callback_url, 'minutes': minutes,
                                         'entity_id': entity_el["_id"], 'scopes': scopes_ids})
            return "Sucesso na Subscription de %s" % callback_url
        else:
            return generic_response.generate_response('ERROR','500','Bad Parameters',
                                                      'subscription','','',entity_name,entity_type,scope_list)
        #####################MONGODB

    except Exception as e:
        error_message = "Erro no registro da Subscription: %s" % (sys.exc_info()[0])
        return generic_response.generate_response('ERROR','500',error_message,
                                                  'subscription','','','','','')


