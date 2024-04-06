from pymongo import MongoClient
from util.constants import *

def save_ibpt(jsonIbpt, ambiente):
    mongoclient = MongoClient(
        host= ambiente.servidor,
        authSource=ambiente.username,
        password=ambiente.passwd
    )
    db = mongoclient[ambiente.db]
    coll_ibpt = db[COLLECTION_IBPT_AUTOMACAO]
    check_is_update_aliquota(coll_ibpt)
    coll_ibpt.insert_many(jsonIbpt)
    mongoclient.close()

def check_is_update_aliquota(collection):
    count = collection.count_documents({})
    if count > 0:
        collection.delete_many({})