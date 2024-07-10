
from infra.database.mongo import get_connection


class UserService:
    def __init__(self):
        self._collection = get_connection()["user"]

    def get_user(self, username):
        user = self._collection.find_one({"username": username})

        return user

    def insert_user(self, user):
        return self._collection.insert_one(user)

    def update_user(self, user):
        self._collection.update_one(
            {"username": user["username"]}, {"$set": user})
