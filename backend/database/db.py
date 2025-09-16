from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["FileStorage"]
collection = db["files"]

print("Connected to local MongoDB")
