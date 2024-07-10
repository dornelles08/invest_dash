import streamlit as st

from functions.login import sing_up, valid_token

st.set_page_config(
    initial_sidebar_state="collapsed"
)

if "token" in st.session_state and "user" in st.session_state:
    token = st.session_state["token"]
    token_is_valid = valid_token(token)
    if token_is_valid:
        st.switch_page("pages/2_dashboard.py")

_, col, _ = st.columns([1, 1, 1])
col.title("Invest Dash")
col.title("")
col.title("")

with st.form("my_form"):
    username = st.text_input("Usuário", value=None)
    name = st.text_input("Nome", value=None)
    password = st.text_input("Senha", type="password", value=None)

    submitted = st.form_submit_button("Cadastrar")
    if submitted:
        if username is not None and password is not None and name is not None:
            success, token, user = sing_up(username, name, password)
            if not success:
                st.warning(token)
            else:                
                st.session_state["user"] = user
                st.session_state["token"] = token
                st.switch_page("pages/2_dashboard.py")
        else:
            st.warning("Há Informações Faltando")
