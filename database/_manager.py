import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv('.env')

class MongoDB:
    instance = None
    def __init__(self) -> None:
        self.mongo_conn_str = os.getenv("MONGO_CONNECTION_STR")
        self.database_name = os.getenv("MONGO_DB_NAME")
        client = MongoClient(self.mongo_conn_str)
        self.db = client[self.database_name]
        
    @staticmethod
    def getDB():
        if not MongoDB.instance:
            MongoDB.instance = MongoDB()
        return MongoDB.instance
    
    def close(self):
        # Connect to MongoDB
        client = MongoClient(self.mongo_conn_str)
        client.close()
        