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
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        con.commit()
        con.close()
        root = ET.Element("contextML")  # Inicio da construcao do XML
        ctxPrvEls = ET.SubElement(root, "ctxPrvEls")
        ctxPrvEl = ET.SubElement(ctxPrvEls, "ctxPrvEl")
        par_scope = ET.SubElement(ctxPrvEl, "par", n="scope")
        par_scope.text = scope
        par_Aproviders = ET.SubElement(ctxPrvEl, "parA", n="contextProviders")
        if len(results) == 0:  # Retorna erro, nao achou nenhum Provider que satisfaz a requisicao
            return generic_response.generate_response('ERROR','400','No results found',
                                                  'getProviders','','','',entity_type,scope)
        if len(entity_type) == 0:  # Caso soh o scope tenha sido definido
            for provider in results:
                par_Sproviders = ET.SubElement(par_Aproviders, "parS", n="contextProvider")
                ET.SubElement(par_Sproviders, "par", n="id").text = provider[0]
                ET.SubElement(par_Sproviders, "par", n="url").text = provider[1]
        else:
            found = False  # variavel local, para caso nao achar nenhum com a entidade desejada
            for provider in results:
                if entity_type in provider[2].split(','):  # provider[2] contem as entidades, separadas por ,
                    found = True  # achou ao menos um
                    par_Sproviders = ET.SubElement(par_Aproviders, "parS", n="contextProvider")
                    ET.SubElement(par_Sproviders, "par", n="id").text = provider[0]
                    ET.SubElement(par_Sproviders, "par", n="url").text = provider[1]
            if not found:
                return generic_response.generate_response('ERROR','400','No results found',
                                                  'getProviders','','','',entity_type,scope)
        xmlString = ET.tostring(root)  # Arvore xml resultante transformada numa str
        return xmlString
    except:
        cursor.close()
        con.commit()
        con.close()
        return generic_response.generate_response('ERROR','500','Internal Server Error',
                                                  'getProviders','','','',entity_type,scope)

