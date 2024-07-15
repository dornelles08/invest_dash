import streamlit as st

from functions.configs import valid_user_logged
from services.transaction import TransactionsService

valid_user_logged()


@st.experimental_dialog("Editar Transação")
def edit_transaction(transaction):
    transactions_service = TransactionsService()

    form = st.form("edit_transaction", clear_on_submit=True)

    ativo = form.text_input("Ativo", value=transaction["Ativo"], disabled=True)
    qtd = form.number_input(
        "Quantidade",  value=transaction["Quantidade"], min_value=0.00)
    price = form.number_input(
        "Preço em R$", value=transaction["Preço"], min_value=0.00)
    date = form.date_input(
        "Data da Compra", transaction["Data da Compra"], format="DD/MM/YYYY")

    col1, col2 = form.columns(2)
    submmited = col1.form_submit_button("Salvar")
    deletar = col2.form_submit_button("Deletar")
    if deletar:
        transactions_service.delete_transaction(
            st.session_state["user"]["_id"], transaction["_id"])
        st.session_state["dados"] = None
        st.rerun()

    if submmited:
        transaction = {
            "_id": transaction["_id"],
            "ativo": ativo,
            "qtd": qtd,
            "price": price,
            "date": date.strftime("%d/%m/%y"),
            "total": round(qtd*price, 2),
            "user_id": st.session_state["user"]["_id"]
        }
        transactions_service.update_transaction(transaction)

        st.success("Transação Atualizada com Sucesso", icon="✅")
        st.session_state["dados"] = None
        st.rerun()
