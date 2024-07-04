from pymongo.mongo_client import MongoClient


def get_connection():
    uri = "mongodb://root:MongoDB!@localhost:27017/"
    client = MongoClient(uri)

    db = client["invest_dash"]

    return db
