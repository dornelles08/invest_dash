import streamlit as st

from functions.login import valid_token

dashboard_page = st.Page("pages/dashboard.py",
                         title="Dashboard", icon=":material/dashboard:")

update_infos_page = st.Page("pages/update/update_infos.py", title="Atualizar Informações",
                            icon=":material/sync_alt:")
update_ativo_page = st.Page("pages/update/update_ativo.py", title="Atualizar Ativo",
                            icon=":material/update:")
insert_new_ativo_page = st.Page("pages/update/insert_new_ativo.py", title="Novo Ativo",
                                icon=":material/add:")

login_page = st.Page("pages/login.py", title="Log in", icon=":material/login:")
logout_page = st.Page("pages/logout.py", title="Log out",
                      icon=":material/logout:")


if "token" in st.session_state and "user" in st.session_state:
    token = st.session_state["token"]
    token_is_valid = valid_token(token)
    if token_is_valid:
        pg = st.navigation(
            {"Dashboard": [dashboard_page],
             "Update": [update_infos_page, update_ativo_page, insert_new_ativo_page],
             "Account": [logout_page]})
    else:
        pg = st.navigation([login_page])
else:
    pg = st.navigation([login_page])

pg.run()
