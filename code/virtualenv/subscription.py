__author__ = 'anderson'
import MySQLdb


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
        return "Sucesso"
    except MySQLdb.Error, e:
        error_message = "<p>Erro no Subscription [%d]: %s</p>" % (e.args[0], e.args[1])
        return error_message
