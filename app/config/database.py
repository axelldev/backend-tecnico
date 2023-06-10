import os
from pymongo import MongoClient

CONN_STRING = os.environ["CONNECTION_STRING"]
client = MongoClient(CONN_STRING)
db = client.api
users_collection = db.users
users_collection.create_index("email", unique=True)
