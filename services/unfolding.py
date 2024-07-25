from infra.database.mongo import get_connection


class UnfoldingService:
    def __init__(self):
        self._collection = get_connection()["unfolding"]

    def get_by_ativo(self, ativo):
        unfolding = self._collection.find_one({"ativo": ativo})

        if not unfolding:
            return None

        return unfolding

    def insert(self, unfolding):
        return self._collection.insert_one(unfolding)

    def update(self, unfolding):
        self._collection.update_one(
            {"ativo": unfolding["ativo"]}, {"$set": unfolding})

    def upsert(self, unfolding):
        exists = self.get_by_ativo(unfolding["ativo"])
        if exists:
            self.update(unfolding)
        else:
            self.insert(unfolding)
