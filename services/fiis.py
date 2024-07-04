from infra.database.mongo import get_connection


class FiisService:
    def __init__(self):
        self._collection = get_connection()["fiis"]

    def get_fiis(self):
        fiis = []
        cursor = self._collection.find()
        for fii in cursor:
            fiis.append(fii)
        return fiis

    def insert_fii(self, fii):
        self._collection.insert_one(fii)

    def update_fii(self, fii):
        self._collection.update_one({"ativo": fii.ativo}, {"$set": {
            "ativo": fii.ativo,
            "qtd": fii.qtd,
            "category": fii.category
        }})
