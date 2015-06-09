__author__ = 'anderson'

from lxml import etree
import os
import logging

# validate_contextML
# dados esperados: string xml
# descricao: analisa o XML para conferir se concorda com o schema ContextML
# retorna: mensagem de sucesso ou erro
def validate_contextml(xml_string):
    logger = logging.getLogger('broker')
    logger.info('validate_contextml - Initiating validation for %s', xml_string)
    with open(os.path.dirname(os.path.abspath(__file__)) + '/ContextML_UKL_v1.0.xsd', 'r') as f:
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)
    xmlparser = etree.XMLParser(schema=schema)
    try:
        etree.fromstring(xml_string, xmlparser)
        return True
    except:
        logger.info('validate_contextml - Failed validation for %s', xml_string)
        return False
