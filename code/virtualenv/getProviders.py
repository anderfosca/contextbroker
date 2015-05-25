__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import ast
import sys
import config
import generic_response

# get_providers
# quem acessa: Consumer
# dados esperados: scope e entity_type(opcional)
# descricao: Consumer faz uma requisicao dos Providers cadastrados no Broker que satisfacam scope e entity_type pedidos
# retorna: xml com ctxPrvEl, com o scope e os Providers que possuem esse scope
# cadastrados
def get_providers(scope, entity_type):
    if len(scope) == 0:
          return generic_response.generate_response('ERROR','400','Bad Parameter',
                                                  'getProviders','','','',entity_type,scope)
    try:    # aqui eh feita a insercao do provider no banco
        con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
        cursor = con.cursor()
        # select de todos os Providers cadastrados no Broker
        sql = "SELECT providers.name, scopes.urlPath, scopes.entityTypes FROM providers, scopes " \
              "WHERE providers.provider_id=scopes.provider_id " \
                                "AND scopes.name = '%s'" % scope
        # TODO validar erro de SQL, devolver msg de erro caso nao ache nada
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        con.commit()
        con.close()
        root = ET.Element("contextML")
        ctxPrvEls = ET.SubElement(root, "ctxPrvEls")
        ctxPrvEl = ET.SubElement(ctxPrvEls, "ctxPrvEl")
        par_scope = ET.SubElement(ctxPrvEl, "par", n="scope")
        par_scope.text = scope
        par_Aproviders = ET.SubElement(ctxPrvEl, "parA", n="contextProviders")
        if len(results) == 0:
            return generic_response.generate_response('ERROR','400','No results found',
                                                  'getProviders','','','',entity_type,scope)
        if len(entity_type) == 0: #caso so o scope tenha sido definido
            for provider in results:
                par_Sproviders = ET.SubElement(par_Aproviders, "parS", n="contextProvider")
                ET.SubElement(par_Sproviders, "par", n="id").text = provider[0]
                ET.SubElement(par_Sproviders, "par", n="url").text = provider[1]
        else: # TODO checar como a entidade eh representada aqui
            found=False
            for provider in results:
                if entity_type in provider[2].split(','):
                    found=True
                    par_Sproviders = ET.SubElement(par_Aproviders, "parS", n="contextProvider")
                    ET.SubElement(par_Sproviders, "par", n="id").text = provider[0]
                    ET.SubElement(par_Sproviders, "par", n="url").text = provider[1]
            if not found:
                return generic_response.generate_response('ERROR','400','No results found',
                                                  'getProviders','','','',entity_type,scope)
        xmlString = ET.tostring(root)   # arvore xml resultante transformada numa str
        return xmlString
    except:
        cursor.close()
        con.commit()
        con.close()
        return generic_response.generate_response('ERROR','500','Internal Server Error',
                                                  'getProviders','','','',entity_type,scope)

