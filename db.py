import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")
if uri is None:
    raise ValueError("MONGODB_URI environment variable not set")

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["WalletWatch"]
except Exception as e:
    print(e)
