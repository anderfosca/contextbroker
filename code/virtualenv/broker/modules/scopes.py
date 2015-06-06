__author__ = 'anderson'

import MySQLdb
import xml.etree.ElementTree as ET
import config
import generic_response

# list_scopes
# dados esperados:
# descricao: lista scopes registrados no broker(? todos, ou atrelados a provider)
# retorna: xml com scopeEls
def list_scopes(provider_name):
    con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cursor = con.cursor()
    # select de todos os Providers cadastrados no Broker
    sql = "SELECT scopes.name FROM scopes " \
          "LEFT JOIN providers ON scopes.provider_id=providers.provider_id " \
          "WHERE providers.name = '%s'" % provider_name
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()
    if len(results) == 0:  # Retorna erro, nao achou nenhum Provider que satisfaz a requisicao
        return generic_response.generate_response('ERROR','400','No scopes found',
                                              'getScopes',provider_name)
    root = ET.Element("contextML")  # Inicio da construcao do XML
    scopeEls = ET.SubElement(root, "scopeEls")
    scopeEl = ET.SubElement(scopeEls, "scopeEl")
    par_Ascopes = ET.SubElement(scopeEl, "parA", n="scopes")
    for scope in results:
        ET.SubElement(par_Ascopes, "par", n="id").text = scope[0]
    xmlString = ET.tostring(root)  # Arvore xml resultante transformada numa str
    return xmlString