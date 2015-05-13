#!flask/bin/python
from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
import MySQLdb
import sys
import getProviders
import advertisement
import getContext
import subscription
import update

broker = Flask(__name__)

# temos aqui as diferentes interfaces do Broker, cada qual corresponde a uma
# funcionalidade

# getProviders
# quem acessa: Consumer
# dados esperados: nenhum
# descricao: Consumer faz uma requisicao dos Providers cadastrados no Broker
# retorna: xml com estrutura de Advertisement, contendo as informacoes dos Providers
# cadastrados
@broker.route('/getProviders', methods=['GET'])
def get_providers():
    xml_string = getProviders.get_providers()
    return jsonify({'providers': xml_string})


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
    message = advertisement.register_provider(broker_info)
    # return codigo de erro, sucesso, etc
    return jsonify({'result': message})

# getContext
# quem usa: Consumer
# dados esperados: parametros URL:
#                               scopeList - lista de scpoes, separados por virgula, sem espacos, nao pode ser vazio
#                                   entities - lista de IDs e tipos, separados pro virgula, sem espaco:
#                                                                           entities=user|joao,user|roberto,
#                                   ou
#                                   entity e type - para so uma entidade: entity=joao&type=user
# descricao:
# retorna: ctxEL mensagem, com os dados que combinem com os parametros, ou uma mensagem de erro
@broker.route('/getContext', methods=['GET'])
def get_context():
    result = getContext.get_context()
    return jsonify({'result': result})

# subscribe
# quem usa: Consumer
# dados esperados: parametros URL:
#                               entity - ID da entidade desejada: entity=joao
#                               type - tipo da entidade desejada: type=user
#                               scopeList - lista de scopes desejados, separados por virgula, sem espaco: location,name
#                               callbackUrl - endereco pra onde o Broker vai enviar dados quando atualizados pelo Prov
#                               time - quantidade de tempo de vida da subscription, em minutos, inteiro maior que 0
# retorna: mensagem de sucesso ou erro
@broker.route('/subscribe', methods=['POST'])
def subscribe():
    result = subscription.subscribe(request.data, request.data)
    return jsonify({'result': result})

# update
# quem usa: Provider
# dados esperados: mensagem XML, validada como ContextML, contendo ctxEL que indica o Provider, entityID e type, scope,
#   timestamp, tempo de vida da informacao, e os dados (dataPart)
# descricao:
# retorna:
@broker.route('/update', methods=['POST'])
def context_update():
    result = update.context_update(request.data)
    return jsonify({'result': result})


if __name__ == '__main__':
    broker.run(debug=True)
