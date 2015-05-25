__author__ = 'anderson'

import xml.etree.ElementTree as ET


def generate_response(status, code, msg, method, provider, provider_version, entity_id, entity_type, scope):
    root = ET.Element("contextML")
    ctxResp = ET.SubElement(root, "ctxResp")
    ET.SubElement(ctxResp, "contextProvider", id=provider, v=provider_version)
    ET.SubElement(ctxResp, "entity", id=entity_id, type=entity_type)
    ET.SubElement(ctxResp, "scope").text = scope
    ET.SubElement(ctxResp, "method").text = method
    ET.SubElement(ctxResp, "resp", status=status, code=code, msg=msg)
    xmlString = ET.tostring(root)   # arvore xml resultante transformada numa str
    return xmlString
