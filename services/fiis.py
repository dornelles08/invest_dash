from infra.database.mongo import get_connection


class FiisService:
    def __init__(self):
        self._collection = get_connection()["fiis"]

    def get_fiis(self, user_id):
        fiis = list(self._collection.find({"user_id": user_id}))

        return fiis

    def insert_fii(self, fii):
        self._collection.insert_one(fii)

    def update_fii(self, fii):
        self._collection.update_one({"ativo": fii["ativo"]}, {"$set": {
            "qtd": fii["qtd"],
            "category": fii["category"]
        }})

    def upsert_fii(self, fii):
        exists_fii = self._collection.find_one({"ativo": fii["ativo"]})
        if exists_fii:
            self.update_fii(fii)
        else:
            self.insert_fii(fii)
