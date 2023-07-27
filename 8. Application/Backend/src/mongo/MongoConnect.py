import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from src.config.Config import Config

class MongoConnect:

    def __init__(self):
        config = Config()
        client = MongoClient(
        f"mongodb://{config.MONGO_USER}:{config.mongo_pass}@{config.MONGO_URL}",
        ssl=True,
        tlsCAFile="cert/mongo.crt"
        )
        self.client = client        
    
    def get_db(self):
        db = self.client[Config.MONGO_DB]
        return db

    def get_collection(self, collection_name):
        collection = self.get_db()[collection_name]
        return collection
    
    def get_request_history(self):
        return self.get_collection('request_history')
    
    def find_one(self, collection, id):
        one = collection.find_one({'_id': ObjectId(id)})
        print(one)
        return one
    
    def get_models(self):
        collection = self.get_db()["model_config"]
        model_config = collection.find_one()
        return model_config["models"]
    

    

    