__author__ = 'anderson'
import MySQLdb
import config
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
        con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
        c = con.cursor()
        c.execute("SELECT entity_id FROM entities WHERE name = '%s'" % entity_name)
        entity_id = c.fetchone()[0]
        c.close()

        c = con.cursor()
        c.execute("INSERT INTO subscriptions(entity_id, callbackUrl, minutes) "
                  "VALUES (%s, %s, %s) ON DUPLICATE KEY "
                      "UPDATE minutes=VALUES(minutes)",
                  (entity_id, callback_url, minutes))
        c.close()
        con.commit()
        for scope in scope_list.split(','):
            c = con.cursor()
            c.execute("INSERT IGNORE INTO scopes_subscriptions(scope_id, subscription_id) "
                      "SELECT scope_id, subscription_id FROM scopes, subscriptions"
                      " WHERE scopes.name='%s' AND subscriptions.callbackUrl='%s'" %
                      (scope, callback_url))
            c.close()
            con.commit()
        con.commit()
        con.close()
        ######################MONGODB
        client = MongoClient()
        db = client.broker
        scopes_collection = db.scopes
        scopes_ids = []
        for result in scopes_collection.find({'name': {'$in' : scope_list.split(',')}}, {'_id': 1}):
            scopes_ids.append(result["_id"])
        entities_collection = db.entities
        entity_el_id = entities_collection.find_one({'name': entity_name}, {'_id': 1})["_id"]
        subscriptions_collection = db.subscriptions
        subscriptions_collection.insert_one(
                                {'callback_url': callback_url, 'minutes': minutes,
                                 'entity_id': entity_el_id, 'scopes': scopes_ids})
        #####################MONGODB
        return "Sucesso na Subscription de %s" % callback_url
    except MySQLdb.Error, e:
        error_message = "<p>Erro no Subscription [%d]: %s</p>" % (e.args[0], e.args[1])
        return error_message


