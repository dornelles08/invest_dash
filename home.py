import streamlit as st

from functions.login import valid_token

dashboard_page = st.Page("pages/dashboard.py",
                         title="Dashboard", icon=":material/dashboard:")

update_base_page = st.Page("pages/update/update_base.py", title="Atualizar Informações",
                           icon=":material/sync_alt:")
update_ativo_page = st.Page("pages/update/update_ativo.py", title="Atualizar Ativo",
                            icon=":material/update:")
insert_new_ativo_page = st.Page("pages/update/insert_new_ativo.py", title="Novo Ativo",
                                icon=":material/add:")

transaction_page = st.Page("pages/transactions/transactions.py",
                           title="Transações",
                           icon=":material/list:")

login_page = st.Page("pages/login.py", title="Log in", icon=":material/login:")
logout_page = st.Page("pages/logout.py", title="Log out",
                      icon=":material/logout:")


if "token" in st.session_state and "user" in st.session_state:
    token = st.session_state["token"]
    token_is_valid = valid_token(token)
    if token_is_valid:
        pg = st.navigation(
            {"Dashboard": [dashboard_page],
             "Atualizações": [insert_new_ativo_page, update_ativo_page, update_base_page],
             "Transações": [transaction_page],
             "Conta": [logout_page]})
    else:
        pg = st.navigation([login_page])
else:
    pg = st.navigation([login_page])

pg.run()
