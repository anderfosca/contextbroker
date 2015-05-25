__author__ = 'anderson'
import config
import MySQLdb

con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
c = con.cursor()
c.execute("SELECT COUNT(*) FROM subscriptions "
                  "LEFT JOIN (entities, scopes, scopes_subscriptions) ON subscriptions.entity_id=entities.entity_id "
                  "AND subscriptions.subscription_id = scopes_subscriptions.subscription_id "
                  "AND scopes.scope_id=scopes_subscriptions.scope_id "
                  "WHERE entities.name='%s' AND entities.type='%s' "
          "AND scopes.name = '%s'" % ("marcos", "username", "test2"))
print c.fetchone()[0]
c.close()
con.commit()