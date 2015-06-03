#!flask/bin/python
from flask import Flask, jsonify, request, render_template
import config
import getProviders
import advertisement as adv
import getContext
import subscription
import update
import contextml_validator
import generic_response
import MySQLdb

broker = Flask(__name__)

# Temos aqui as diferentes interfaces do Broker, cada qual corresponde a uma funcionalidade

# getProviders
# quem acessa: Consumer
# dados esperados: nenhum
# descricao: Consumer faz uma requisicao dos Providers cadastrados no Broker
# retorna: xml com estrutura de Advertisement, contendo as informacoes dos Providers
# cadastrados
@broker.route('/getProviders', methods=['GET'])
def get_providers():
    scope = request.args.get('scope')
    entity_type = request.args.get('entity')
    result = getProviders.get_providers(scope, entity_type)
    return result


# advertisement
# quem usa: Provider
# dados esperados: xml com informacoes do Provider
# descricao: Faz o registro (ou atualizacao) das informacoes do Provider que enviou os dados, caso seja um segundo Adv,
#   os dados serao tratados como os mais atuais, substituindo os anteriores. O Provider deve manter contato com o Broker
#   de tempos em tempos, o Broker tem um timer que, caso nao haja interacao no tempo, o Broker pede um sinal de vida ao
#   Provider, na forma de ACK
# retorna: mensagem de sucesso ou erro
@broker.route('/advertisement', methods=['POST'])
def advertisement():
    broker_info = request.data
    if contextml_validator.validate_contextml(broker_info):
        result = adv.register_provider(broker_info)
    else:
        result = generic_response.generate_response('ERROR','400','Bad XML','advertisement')
    print result
    # return codigo de erro, sucesso, etc
    return result

# getContext
# quem usa: Consumer
# dados esperados: parametros URL:
#                               scopeList - lista de scpoes, separados por virgula, sem espacos, nao pode ser vazio
#                                   entities - lista de IDs e tipos, separados pro virgula, sem espaco:
#                                                                           entities=user|joao,user|roberto,
#                                   ou
#                                   entity e type - para so uma entidade: entity=joao&type=user
# descricao: Consumer pede por dados que satisfacam os Scopes e entidades listadas nos parametros
# retorna: ctxEL mensagem, com os dados que combinem com os parametros, ou uma mensagem de erro
@broker.route('/getContext', methods=['GET'])
def get_context():
    scope_list = request.args.get('scopeList')
    if request.args.get('entities'):
        entities = request.args.get('entities')
    else:
        entities = request.args.get('type') + '|' + request.args.get('entity')
    result = getContext.get_context(scope_list, entities)
    print result
    return result

# subscribe
# quem usa: Consumer
# dados esperados: parametros URL:
#                               entity - ID da entidade desejada: entity=joao
#                               type - tipo da entidade desejada: type=user
#                               scopeList - lista de scopes desejados, separados por virgula, sem espaco: location,name
#                               callbackUrl - endereco pra onde o Broker vai enviar dados quando atualizados pelo Prov
#                               time - quantidade de tempo de vida da subscription, em minutos, inteiro maior que 0
# descricao: Consumer envia entidade e escopos sobre os quais deseja receber atualizacoes, na sua Url, e um tempo de
#   vida para a subscription
# retorna: mensagem de sucesso ou erro
@broker.route('/subscribe', methods=['GET'])
def subscribe():
    entity_id = request.args.get('entity')
    entity_type = request.args.get('type')
    scope_list = request.args.get('scopeList')
    callback_url = request.args.get('callbackUrl')
    minutes = request.args.get('time')
    result = subscription.subscribe(callback_url, entity_id, entity_type, scope_list, minutes)
    return result

# update
# quem usa: Provider
# dados esperados: mensagem XML, contendo ctxEL que indica o Provider, entityID e type, scope,
#   timestamp, tempo de vida da informacao, e os dados (dataPart)
# descricao: valida XML como sendo ContextML
# retorna:
@broker.route('/update', methods=['POST'])
def context_update():
    update_xml = request.data
    if contextml_validator.validate_contextml(update_xml):
        result = update.context_update(update_xml)
    else:
        result = generic_response.generate_response('ERROR','400','Bad XML','update')
    return result


#index
@broker.route('/')
def index():
    return render_template("index.html")


#index
@broker.route('/providers')
def providers():
    con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cursor = con.cursor()
    # select de todos os Providers cadastrados no Broker
    sql = "SELECT name, url, version, location, location_desc" \
          " FROM providers"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()
    return render_template("providers.html", results=results)

#subscriptions
@broker.route('/subscriptions')
def subscriptions():
    con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cursor = con.cursor()
    # select de todos os Providers cadastrados no Broker
    sql = "SELECT callbackUrl, minutes" \
          " FROM subscriptions"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()
    return render_template("subscriptions.html", results=results)

#registrytable
@broker.route('/registers')
def registers():
    con = MySQLdb.connect(host=config.db_host, user=config.db_user, passwd=config.db_password, db=config.db_name)
    cursor = con.cursor()
    # select de todos os Providers cadastrados no Broker
    sql = "SELECT providers.name, scopes.name, entities.type, entities.name, registryTable.dataPart" \
          " FROM registryTable, scopes, entities,providers " \
          "WHERE providers.provider_id=registryTable.provider_id AND scopes.scope_id=registryTable.scope_id " \
          "AND entities.entity_id=registryTable.entity_id"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()
    return render_template("registers.html", results=results)

# before_request
# descricao: realiza o que estiver aqui antes de qualquer request, seja GET ou POST, tanto faz
@broker.before_request
def before_request():
    print "before_request"


# TODO timers que ficam contando os expires, etc
# TODO sistema de log
# TODO telas para visualizar a tabela de Registros e a de Providers
# TODO docstring
if __name__ == '__main__':
    broker.run(debug=True, use_reloader=True)
    # broker.run(threaded=True)

