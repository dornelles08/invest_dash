
from infra.database.mongo import get_connection


class DadosService:
    def __init__(self):
        self._collection = get_connection()["dados"]

    def get_dados(self):
        dados = []
        cursor = self._collection.find()
        for dado in cursor:
            dados.append(dado)
        return dados

    def insert_dado(self, dado):
        self._collection.insert_one(dado)

    def insert_dados(self, dados):
        self._collection.insert_many(dados)
