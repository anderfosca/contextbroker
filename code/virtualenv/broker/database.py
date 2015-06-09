__author__ = 'anderson'
import pymongo
from pymongo import MongoClient, ASCENDING, DESCENDING

def configure_database():
    client = MongoClient()
    db = client.broker
    db.providers.create_index('name', unique=True)
    db.providers.create_index('url', unique=True)
    db.scopes.create_index('url_path', unique=True)
    db.subscriptions.create_index([('entity_id', ASCENDING), ('callback_url', DESCENDING)], unique=True)
    db.entities.create_index([('name', ASCENDING), ('type', ASCENDING)], unique=True)
    db.registries.create_index([('provider_id', ASCENDING), ('scope_id', ASCENDING), ('entity_id', ASCENDING)],
                               unique=True)
    db.providers.remove()
    db.scopes.remove()
    db.entities.remove()
    db.registries.remove()
    db.subscriptions.remove()

