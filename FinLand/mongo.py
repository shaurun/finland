#This file handles connection with mongoDB

from pymongo import MongoClient


class MongoDBClient:

    def __init__(self, host, port):
        self.client = MongoClient(host, port)

    def connect(self, database):
        self.db = self.client[database]
        print("Connected to database")

    def insert_document(self, collection, document):
        db_collection = self.db[collection]
        document_id = db_collection.insert_one(document).inserted_id
        return document_id

    def insert_all(self, collection, documents):
        db_collection = self.db[collection]
        document_ids = db_collection.insert_many(documents).inserted_ids
        return document_ids

    def find_document(self, collection, document_identifier):
        db_collection = self.db[collection]
        return db_collection.find_one(document_identifier)

    def find_all(self, collection: str, document_identifier):
        db_collection = self.db[collection]
        return db_collection.find(document_identifier)

    def update_document(self, collection, document_identifier, update_info):
        db_collection = self.db[collection]
        db_collection.update_one(document_identifier, update_info, upsert=True)

    def __del__(self):
        self.client.close()
        print("Disconnected from database")
