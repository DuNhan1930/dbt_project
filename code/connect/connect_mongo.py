import os
from pymongo import MongoClient

mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["glamira_db"]

print(client.list_database_names())
print(db.list_collection_names())
