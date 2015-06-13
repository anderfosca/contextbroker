__author__ = 'anderson'

import xml.etree.ElementTree as ET
import generic_response
import pymongo
from pymongo import MongoClient

# list_scopes
# dados esperados:
# descricao: lista scopes registrados no broker(? todos, ou atrelados a provider)
# retorna: xml com scopeEls
def list_scopes(provider_name):
    #####################MONGODB
    client = MongoClient()
    db = client.broker
    providers_collection = db.providers
    provider = providers_collection.find_one({'name': provider_name}, {'_id': 1})
    if provider is not None:
        scopes = db.scopes.find(
            {'provider_id': provider["_id"]})
        if scopes.count() == 0:  # Retorna erro, nao achou nenhum Provider que satisfaz a requisicao
            return generic_response.generate_response('ERROR','404','No scopes found',
                                                      'getScopes',provider_name)
    #####################MONGODB

        root = ET.Element("contextML")  # Inicio da construcao do XML
        scopeEls = ET.SubElement(root, "scopeEls")
        scopeEl = ET.SubElement(scopeEls, "scopeEl")
        par_Ascopes = ET.SubElement(scopeEl, "parA", n="scopes")
        for scope in scopes:
            ET.SubElement(par_Ascopes, "par", n="id").text = scope['name']

        xmlString = ET.tostring(root)  # Arvore xml resultante transformada numa str
        return xmlString
    else:
         return generic_response.generate_response('ERROR','400','Bad paramenter',
                                                   'getScopes',provider_name)