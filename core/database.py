from pymongo import MongoClient
from core.config import MONGODB_URI, MONGODB_DATABASE

client = MongoClient(MONGODB_URI)

database = client[MONGODB_DATABASE]

productos_collection = database["productos"]