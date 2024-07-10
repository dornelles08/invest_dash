
from infra.database.mongo import get_connection


class DadosService:
    def __init__(self):
        self._collection = get_connection()["dados"]

    def get_dados(self, fiis_names):
        dados = list(self._collection.find({"nome": {"$in": fiis_names}}))

        return dados

    def insert_dado(self, dado):
        self._collection.insert_one(dado)

    def insert_dados(self, dados):
        self._collection.insert_many(dados)

    def update_dado(self, dado):
        self._collection.update_one({"nome": dado["nome"]}, {"$set": dado})

    def upsert_dado(self, dado):
        exists_data = self._collection.find_one({"nome": dado["nome"]})
        if exists_data:
            self.update_dado(dado)
        else:
            self.insert_dado(dado)

    def upsert_dados(self, dados):
        for dado in dados:
            self.upsert_dado(dado)
