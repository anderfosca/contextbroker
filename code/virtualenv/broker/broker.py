#!flask/bin/python
from flask import Flask, jsonify, request, render_template
import modules.getProviders as getProviders
import modules.advertisement as adv
import modules.getContext as getContext
import modules.subscription as subscription
import modules.update as update
import modules.contextml_validator as contextml_validator
import modules.generic_response as generic_response
import logging
from logging.handlers import RotatingFileHandler
import os
import pymongo
from pymongo import MongoClient

broker = Flask('broker')

# Logging initialization
logger = logging.getLogger('broker')
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler(os.path.dirname(os.path.abspath(__file__)) + '/log/broker',
                                   maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



# Broker Interfaces

# getProviders
# quem acessa: Consumer
# dados esperados: nenhum
# descricao: Consumer faz uma requisicao dos Providers cadastrados no Broker
# retorna: xml com estrutura de Advertisement, contendo as informacoes dos Providers
# cadastrados
# Receives GET message, with scope and entity arguments, searches the database for Providers associated with the
# arguments, returns ContextML Providers information message or ERROR ContextML message
@broker.route('/getProviders', methods=['GET'])
def get_providers():
    scope = request.args.get('scope')
    entity_type = request.args.get('entity')
    logger.info('getProviders - scope: '+scope+' entity_type: '+entity_type)
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
# Receives ContextML advertisement message, validates it, registers the Provider and Scopes on the database, returns OK
# or ERROR ContextML message
@broker.route('/advertisement', methods=['POST'])
def advertisement():
    # TODO ->>>>>>>>>>>>avisa os outros que recebeu
    xml_string = request.data
    if contextml_validator.validate_contextml(xml_string):
        result = adv.register_provider(xml_string)
    else:
        logger.warn('advertisement - XML not accepted by ContextML Schema')
        result = generic_response.generate_response('ERROR','400','Bad XML','advertisement')
    return result
    #return jsonify({'result': result})

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
# Receives a GET message, with scopeList and entities, or, entity and type arguments, searches for the content in
# the database, if not found asks the Providers associated with the arguments, returns the elements queried or ERROR
# ContextML message
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
# Receives a GET message, with entity, type, scopeList, callbackUrl and time arguments in the URL, registers
# the Subscription and returns OK or ERROR ContextML message
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
# Receives a ContextML message, validates it, makes the update in the database, returns OK or ERROR ContextML message.
@broker.route('/update', methods=['POST'])
def context_update():
    update_xml = request.data
    if contextml_validator.validate_contextml(update_xml):
        result = update.context_update(update_xml)
    else:
        logger.warn('update - XML not accepted by ContextML Schema')
        result = generic_response.generate_response('ERROR','400','Bad XML','update')
    return result


# Index page of the Broker, has links to Providers, Subscriptions, Registries and Log pages
@broker.route('/')
def index():
    return render_template("index.html")


# Gets and shows the Providers in the providers.html template
@broker.route('/providers')
def providers():
    ##################MONGODB
    answ = MongoClient().broker.providers.find()
    ##################MONGODB
    return render_template("providers.html", answ=answ)

# Gets and shows the Subscriptions in the subscriptions.html template
@broker.route('/subscriptions')
def subscriptions():
    ###############MONGODB
    answ = MongoClient().broker.subscriptions.find()
    ###############MONGODB
    return render_template("subscriptions.html", answ=answ)


# Gets and shows the Registries in the registries.html template
@broker.route('/registers')
def registers():
    ###############MONGODB
    answ = MongoClient().broker.registries.find()
    ###############MONGODB

    return render_template("registers.html", answ=answ)


# Shows the log file content, in the log.html template
@broker.route('/log')
def log_page():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/log/broker', 'r') as f:
        log_string = f.read()
    return render_template("log.html", log_string=log_string)

# heartbeat
@broker.route('/heartbeat')
def heartbeat():
    return "OK"

# before_request
# descricao: realiza o que estiver aqui antes de qualquer request, seja GET ou POST, tanto faz
@broker.before_request
def before_request():
    args = request.args
    data = request.data
    print "before_request "
    print args, data
    # enviar info do request para os brothers

@broker.after_request
def per_request_callbacks(response):
    print "after_request"
    print request.args
    print response.data

    # avisar os brothers que finalizou o request
    return response

@broker.route('/tf_message')
def tf_message():
    # tem que haver uma autenticacao do Broker irmao, pra nao virar alvo de ataques
    # recebe a mensagem, extrai os valores que importam, salva numa HashTable em memoria mesmo
    # salva so uma mensagem de cada broker, a ultima, pois se o outro Broker confirma a execucao de uma tarefa,
    #   ela nao interessa mais, entao quando ele manda outra ja pode guardar por cima, assim nao ocupa muito espaco
    # nao precisa recuperar estado porque eh stateless
    return 'bla'

# --------background function
# ----funcao que faz a TF
# 1 manda HB pra um brother
#   checa se ele responde
#   se sim
#       espera 5s
#       volta pra 1
#   senao
#       chama ele de novo
#       se respondeu
#           espera 5s
#           volta pra 1
#       senao
#           pega ultima msg do brother
#           confere se ela eh um "ok eu fiz meu bagulho" OU se eh um "faz isso ai brother"
#           se eh um "ok eu fiz meu bagulho"
# 2             manda HB
#               se respondeu
#                   espera 5s
#                       volta pra 2
#               senao respondeu
#                   volta pra 2
#           se eh um "faz isso ai brother"
#               avisa os outros bkps que vai "fazer isso"
#               faz "isso"
#               avisa os outros que fez
# 3             manda HB pro brother
#               se respondeu
#                   espera 5s
#                   volta pra 1
#               senao
#                   volta pra 3
#
#


# TODO timers que ficam contando os expires, etc
# TODO docstring
if __name__ == '__main__':
    logger.info('Started')
    client = MongoClient()
    db = client.broker
    db.providers.remove()
    db.scopes.remove()
    db.entities.remove()
    db.registries.remove()
    db.subscriptions.remove()

    broker.run(debug=True, use_reloader=True, threaded=True)

