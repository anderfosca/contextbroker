__author__ = 'anderson'

import sys
import MySQLdb


# getContext
# dados esperados: scopeList - lista de scpoes, separados por virgula, sem espacos, nao pode ser vazio
#                  entities - lista de IDs e tipos, separados pro virgula, sem espaco:
#                                                                           entities=user|joao,user|roberto,...
# descricao: procura na tabela de registros o ultimo registro que corresponde aos parametros dados
# retorna: ctxEL mensagem, com os dados que combinem com os parametros, ou uma mensagem de erro
def get_context(scope_list, entities):
    try:
        con = MySQLdb.connect(host='localhost', user='broker_manager', passwd='senhamanager', db='broker')

    except:
        e = sys.exc_info()[0]
        error_message = "<p>Erro no Update: %s</p>" % e
        return error_message
