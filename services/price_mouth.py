from infra.database.mongo import get_connection


class PriceMonthService:
    def __init__(self):
        self._collection = get_connection()["price_by_month"]

    def get_by_ativo(self, ativo):
        price_month = self._collection.find_one({"ativo": ativo})

        if not price_month:
            return None

        return {"ativo": price_month["ativo"], "price_month": price_month["valor_por_mes"]}

    def get_by_ativos(self, ativos):
        prices_months = []
        for ativo in ativos:
            price_month = self.get_by_ativo(ativo)
            prices_months.append(price_month)

        return prices_months

    def insert(self, price_month):
        return self._collection.insert_one(price_month)

    def update(self, price_month):
        self._collection.update_one(
            {"ativo": price_month["ativo"]}, {"$set": price_month})

    def upsert(self, price_month):
        exists = self.get_by_ativo(price_month["ativo"])
        if exists:
            self.update(price_month)
        else:
            self.insert(price_month)
