from infra.database.mongo import get_connection


class TransactionsService:
    def __init__(self):
        self._collection = get_connection()["transactions"]

    def get_transactions(self, user_id, filtro={}):
        transactions = self._collection.find({"user_id": user_id, **filtro})

        return list(transactions)

    def count_transactions(self, user_id):
        count = self._collection.count_documents({"user_id": user_id})

        return count

    def get_fiis_from_transactions(self, user_id):
        transactions = self._collection.distinct("ativo", {"user_id": user_id})

        return list(transactions)

    def insert_transaction(self, transaction):
        self._collection.insert_one(transaction)

    def update_transaction(self, transaction):
        self._collection.update_one(
            {"_id": transaction["_id"]}, {"$set": transaction})

    def upsert_transaction(self, transaction):
        exists_transaction = self._collection.find_one(
            {"_id": transaction["_id"]})
        if exists_transaction:
            self.update_transaction(transaction)
        else:
            self.insert_transaction(transaction)

    def delete_transaction(self, user_id, _id):
        self._collection.delete_one({"_id": _id, "user_id": user_id})
