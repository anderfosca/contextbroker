__author__ = 'anderson'
import MySQLdb
import config

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
                  "VALUES (%s, %s, %s)",
                  (entity_id, callback_url, minutes))
        c.close()
        con.commit()
        for scope in scope_list.split(','):
            c = con.cursor()
            c.execute("SELECT scope_id FROM scopes WHERE name = '%s'" % scope)
            scope_id = c.fetchone()[0]
            c.close()
            c = con.cursor()
            c.execute("SELECT subscription_id FROM subscriptions WHERE callbackUrl = '%s'" % callback_url)
            subscription_id = c.fetchone()[0]
            c.close()
            c = con.cursor()
            c.execute("INSERT INTO scopes_subscriptions(scope_id, subscription_id) "
                      "VALUES (%s, %s)",
                      (scope_id, subscription_id))
            c.close()
            con.commit()
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
def check_subscriptions(entity_name, entity_type, scope):
    try:
        # TODO validar os campos, url ser URL, entidade e escopo(s) existirem de fato
        con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
        c = con.cursor()
        c.execute("SELECT callbackUrl FROM subscriptions "
                  "LEFT JOIN (entities, scopes, scopes_subscriptions) ON subscriptions.entity_id=entities.entity_id "
                  "AND subscriptions.subscription_id = scopes_subscriptions.subscription_id "
                  "AND scopes.scope_id=scopes_subscriptions.scope_id "
                  "WHERE entities.name='%s' AND entities.type='%s' "
                  "AND scopes.name='%s'" % (entity_name, entity_type, scope))
        callbacks = c.fetchall()
        c.close()
        con.commit()
        con.close()
        for url in callbacks:
            print url[0]
        return callbacks

    except MySQLdb.Error, e:
        error_message = "<p>Erro no Subscription [%d]: %s</p>" % (e.args[0], e.args[1])
        return False
