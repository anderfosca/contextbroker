__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import sys
import re
import subscription
import requests
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
def context_update(xml_string_original):
    xml_string = re.sub(' xmlns="[^"]+"', '', xml_string_original, count=1)
    xml_string = re.sub(' xmlns:xsi="[^"]+"', '', xml_string, count=1)
    xml_string = re.sub(' xsi:schemaLocation="[^"]+"', '', xml_string, count=1)
    root = ET.fromstring(xml_string)

    try:
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
                c.execute("SELECT provider_id FROM providers WHERE name = '%s'" % nameProv)
                provider_id = c.fetchone()[0]
                c.close()
                c = con.cursor()
                c.execute("SELECT scope_id FROM scopes WHERE name = '%s' AND provider_id = '%s'" % (scope,provider_id))
                scope_id = c.fetchone()[0]
                c.close()
                c = con.cursor()
                c.execute("INSERT INTO entities(name, type)"
                          " VALUES (%s, %s)", (entityId, entityType))
                c.close()
                c = con.cursor()
                c.execute("SELECT entity_id FROM entities WHERE name = '%s'" % entityId)
                entity_id = c.fetchone()[0]
                c.close()
                c = con.cursor()
                c.execute("INSERT INTO registryTable(provider_id, scope_id, entity_id, timestamp, expires, dataPart)"
                          " VALUES (%s, %s, %s, %s, %s, %s)",
                          (provider_id, scope_id, entity_id, timestamp, expires, dataPart))
                c.close()
                con.commit()
                con.close()
                #return "Sucesso no Update"
                # TODO
                callbacks = subscription.check_subscriptions(entityId, entityType, scope)
                #if length(callbacks) > 0:
                #   enviar esse ctxEl para o Consumer subscripted
                for url in callbacks:
                    send_to_consumer(url[0], xml_string_original)
                return "Sucesso e subscripteds atualizados"
                #else:
                 #   return "Sucesso nenhum subscripted"
            except: # catch *all* exceptions
                e = sys.exc_info()[0]
                error_message = "<p>Erro no Update: %s</p>" % e
                return error_message
    except:
        e = sys.exc_info()[0]
        error_message = "<p>Erro no Update: %s</p>" % e
        return error_message


