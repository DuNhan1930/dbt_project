from pymongo import MongoClient

client = MongoClient(
    "mongodb://duadmin:strongpassword123@34.87.143.250:27017/?authSource=admin&tls=true",
    tlsCAFile="/home/dunhan/Downloads/mongodb-cert.crt"
)

db = client["glamira_db"]

print(client.list_database_names())
print(db.list_collection_names())
