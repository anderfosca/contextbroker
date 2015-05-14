__author__ = 'anderson'
import MySQLdb


def subscribe(callback_url, entity_id, entity_type, scope_list, time):
    try:
        con = MySQLdb.connect(host='localhost', user='root', passwd='showtime', db='broker')
        c = con.cursor()
        c.execute("INSERT INTO subscriptions(callbackUrl, entityID, entityType, scopeList, time) "
                  "VALUES (%s, %s, %s, %s, %s)",
                  (callback_url, entity_id, entity_type, scope_list, time))
        c.close()
        con.commit()
        con.close()
        return "Sucesso"
    except MySQLdb.Error, e:
        error_message = "<p>Erro no registro do Provider %s [%d]: %s</p>" % (nameProv, e.args[0], e.args[1])
        return error_message