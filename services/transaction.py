from infra.database.mongo import get_connection


class TransactionsService:
    def __init__(self):
        self._collection = get_connection()["transactions"]

    def get_transactions(self, user_id):
        transactions = list(self._collection.find({"user_id": user_id}))

        return transactions

    def insert_transaction(self, transaction):
        self._collection.insert_one(transaction)

    def update_transaction(self, transaction):
        self._collection.update_one({"ativo": transaction["ativo"]}, {"$set": {
            "qtd": transaction["qtd"],
            "category": transaction["category"]
        }})

    def upsert_transaction(self, transaction):
        exists_transaction = self._collection.find_one(
            {"ativo": transaction["ativo"]})
        if exists_transaction:
            self.update_transaction(transaction)
        else:
            self.insert_transaction(transaction)
