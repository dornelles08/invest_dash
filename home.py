import streamlit as st

from functions.login import valid_token

dashboard_page = st.Page("pages/dashboard.py",
                         title="Dashboard", icon=":material/dashboard:")

# desdobramento_page = st.Page("pages/update/desdobramento.py", title="Desdobramento",
#                              icon=":material/contract:")

patrimony_page = st.Page("pages/patrimony.py", title="Patrimonio",
                         icon=":material/attach_money:")

position_detailed = st.Page("pages/position/detailed.py", title="Posição Detalhada",
                            icon=":material/open_in_full:")
position_summarized = st.Page("pages/position/summarized.py", title="Posição Resumida",
                              icon=":material/close_fullscreen:")

profit_page = st.Page("pages/profit.py", title="Rentabilidade",
                      icon=":material/query_stats:")

update_ativo_page = st.Page("pages/ativo/update_ativo.py", title="Atualizar Ativo",
                            icon=":material/update:")

transaction_page = st.Page("pages/transactions/transactions.py",
                           title="Transações",
                           icon=":material/list:")

test_page = st.Page("pages/test.py",
                    title="Teste",
                    icon=":material/bug_report:")

login_page = st.Page("pages/login.py", title="Log in", icon=":material/login:")
singup_page = st.Page("pages/cadastrar.py",
                      title="Sing up", icon=":material/login:")
logout_page = st.Page("pages/logout.py", title="Log out",
                      icon=":material/logout:")

page_stack = {
    "Dashboard": [dashboard_page],
    "Patrimoio": [patrimony_page],
    # "Atualizações": [desdobramento_page],
    "Posição": [position_summarized, position_detailed],
    "Rentabilidade": [profit_page],
    "Ativo": [update_ativo_page],
    "Transações": [transaction_page],
    "Testes": [test_page],
    "Conta": [logout_page]
}

if "token" in st.session_state and "user" in st.session_state:
    token = st.session_state["token"]
    TOKEN_IS_VALID = valid_token(token)
    if TOKEN_IS_VALID:
        pg = st.navigation(page_stack)
    else:
        pg = st.navigation([login_page, singup_page])
else:
    pg = st.navigation([login_page, singup_page])

pg.run()
