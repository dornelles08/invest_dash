import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()


def get_connection():
    mongo_string = os.getenv('MONGO_STRING')
    client = MongoClient(mongo_string)

    db = client["invest_dash"]

    return db
