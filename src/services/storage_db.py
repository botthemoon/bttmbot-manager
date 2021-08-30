import json

from pymongo import MongoClient

from src.settings import mongo_host, mongo_db


class StorageDB():
    def __init__(self):
        self.client = MongoClient(mongo_host, 27017)
        self.db = self.client[mongo_db]

    def close_conection(self):
        self.client.close()


db = client['countries_db']
collection_currency = db['currency']

with open('currencies.json') as f:
    file_data = json.load(f)

# if pymongo < 3.0, use insert()
collection_currency.insert(file_data)
# if pymongo >= 3.0 use insert_one() for inserting one document
collection_currency.insert_one(file_data)
# if pymongo >= 3.0 use insert_many() for inserting many documents
collection_currency.insert_many(file_data)

client.close()
