__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import sys
import re
import subscription
import generic_response
import config

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
            con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
            c = con.cursor()
            c.execute("SELECT scopes.scope_id, scopes.provider_id FROM scopes "
                      "LEFT JOIN providers ON scopes.provider_id=providers.provider_id "
                      "WHERE scopes.name = '%s' AND providers.name = '%s'" % (scope, nameProv))
            result = c.fetchone()
            if len(result) == 0:  # caso nao ache o scope
                c.close()
                con.close()
                return generic_response.generate_response('ERROR','400','Bad parameters','update',nameProv,version,entityId,entityType,scope)
            scope_id = result[0]
            provider_id = result[1]
            c.close()
            c = con.cursor()
            c.execute("INSERT IGNORE INTO entities(name, type)"  # insere soh uma vez a dupla nome-tipo pra entidade
                      " VALUES (%s, %s)",
                      (entityId, entityType))
            c.close()
            c = con.cursor()
            c.execute("SELECT entity_id FROM entities WHERE name = '%s' AND type='%s'" % (entityId, entityType))
            entity_id = c.fetchone()[0]
            c.close()
            c = con.cursor()
            c.execute("INSERT INTO registryTable(provider_id, scope_id, entity_id, timestamp, expires, dataPart)"
                      " VALUES (%s, %s, %s, %s, %s, %s)",
                      (provider_id, scope_id, entity_id, timestamp, expires, dataPart))
            c.close()
            con.commit()
            con.close()
            # hora de conferir as subscriptions
            callbacks = check_subscriptions(entityId, entityType, scope)
            if len(callbacks) > 0:
                for url in callbacks:
                    send_to_consumer(url[0], xml_string_original)
                return generic_response.generate_response('OK','200','Update and subscription success','update',nameProv,version,entityId,entityType,scope)
            else:
                return generic_response.generate_response('OK','200','Update success','update',nameProv,version,entityId,entityType,scope)
        except MySQLdb.Error, e:
            c.close()
            con.commit()
            con.close()
            error_message = "<p>Erro no Update [%d]: %s</p>" % (e.args[0], e.args[1]) # catch *all* exceptions
            return generic_response.generate_response('ERROR','400','Update failed '+error_message,'update',nameProv,version,entityId,entityType,scope)

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
