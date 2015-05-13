__author__ = 'anderson'

import xml.etree.ElementTree as ET
import MySQLdb
import sys

# register_provider
# dados esperados: xml com informacoes do Provider
# descricao: Faz o registro (ou atualizacao) das informacoes do Provider que enviou
# os dados
# retorna: mensagem de sucesso ou erro
def register_provider(broker_info):
    root = ET.fromstring(broker_info)
    try:
        for adv in root.find('ctxAdvs').findall('ctxAdv'):  # tratar casos de mais de um Provider ter sido advertido
            try:
                nameProv = adv.find('contextProvider').get('id')
                version = adv.find('contextProvider').get('v')
                urlRoot = adv.find('urlRoot').text
                lat, lon, location = '', '', ''
                if adv.find('providerLocation') is not None:    # Location pode nao ter sido anunciada
                    lat = adv.find('providerLocation').find('lat').text
                    lon = adv.find('providerLocation').find('lon').text
                    location = adv.find('providerLocation').find('location').text
                try:    # aqui eh feita a insercao do provider no banco
                    con = MySQLdb.connect(host='localhost', user='root', passwd='showtime', db='broker')
                    c = con.cursor()
                    c.execute("INSERT INTO providers(name, url, version, location, location_desc) VALUES (%s, %s, %s, %s, %s)",
                              (nameProv, urlRoot, version, lat+";"+lon, location))
                    c.close()
                    con.commit()
                    con.close()
                except MySQLdb.Error, e:
                    error_message = "<p>Erro no registro do Provider %s [%d]: %s</p>" % (nameProv, e.args[0], e.args[1])
                    return error_message
                # a partir daqui sao inseridos os scopes, na tabela de scopes
                for scope in adv.find('scopes').findall('scopeDef'):
                    name_scope = scope.get('n')
                    url_path = scope.find('urlPath').text
                    entity_types = scope.find('entityTypes').text
                    inputs = []
                    for inputEl in scope.find('inputDef').findall('inputEl'):   # inputs sao colocados juntos em string
                        input_name = inputEl.get('name')
                        input_type = inputEl.get('type')
                        inputs.append(input_name+";"+input_type)
                    con = MySQLdb.connect(host='localhost', user='root', passwd='showtime', db='broker')
                    c = con.cursor()
                    c.execute("SELECT provider_id FROM providers WHERE name = '%s'" % nameProv)
                    provider_id = c.fetchone()[0]
                    c.close()
                    try:
                        c = con.cursor()
                        c.execute("INSERT INTO scopes (name, urlPath, entityTypes, inputs, provider_id)"
                                  "          VALUES (%s, %s, %s, %s, %s)",
                                  (name_scope, url_path, entity_types, str(inputs), provider_id))
                        c.close()
                    except MySQLdb.Error, e:
                        con.commit()
                        con.close()
                        error_message = "<p>Erro no registro do Scope %s [%d]: %s</p>" % (name_scope, e.args[0], e.args[1])
                        return error_message
            except: # TODO reduzir escopo da excecoes
                con.commit()
                con.close()
                e = sys.exc_info()[0]
                error_message = "<p>Erro no Advertisement: %s</p>" % e
                return error_message
        con.commit()
        con.close()
        return "Sucesso"
    except: # TODO reduzir escopo da excecoes
        e = sys.exc_info()[0]
        error_message = "<p>Erro no Advertisement: %s</p>" % e
        return error_message
