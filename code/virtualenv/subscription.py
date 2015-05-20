__author__ = 'anderson'
import MySQLdb


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
def subscribe(callback_url, entity_id, entity_type, scope_list, minutes):
    try:
        # TODO validar os campos, url ser URL, entidade e escopo(s) existirem de fato
        con = MySQLdb.connect(host='localhost', user='broker_manager', passwd='senhamanager', db='broker')
        c = con.cursor()
        c.execute("INSERT INTO subscriptions(callbackUrl, entityID, entityType, scopeList, minutes) "
                  "VALUES (%s, %s, %s, %s, %s)",
                  (callback_url, entity_id, entity_type, scope_list, minutes))
        c.close()
        con.commit()
        con.close()
        return "Sucesso na Subscription de %s" % callback_url
    except MySQLdb.Error, e:
        error_message = "<p>Erro no Subscription [%d]: %s</p>" % (e.args[0], e.args[1])
        return error_message


# check_subscriptions
# dados esperados: entity, scope
# descricao: Consumer envia entidade e escopos sobre os quais deseja receber atualizacoes, na sua Url, e um tempo de
#   vida para a subscription
# # retorna: mensagem de sucesso ou erro
def check_subscriptions(entity_id, entity_type, scope):
    try:
        # TODO validar os campos, url ser URL, entidade e escopo(s) existirem de fato
        con = MySQLdb.connect(host='localhost', user='broker_manager', passwd='senhamanager', db='broker')
        c = con.cursor()
        c.execute("SELECT callbackUrl, scopeList FROM subscriptions "
                  "WHERE entityID = '%s' AND entityType = '%s'" % (entity_id, entity_type))
        elements = c.fetchone()
        c.close()
        con.commit()
        con.close()
        # TODO
        # dividir scopeList
        # checar se o scope em questao esta incluso nesse scopeList
        # se sim, retorna true

        return "Sucesso na Subscription"
    except MySQLdb.Error, e:
        error_message = "<p>Erro no Subscription [%d]: %s</p>" % (e.args[0], e.args[1])
        return error_message
