import streamlit as st

from functions.login import login

_, col, _ = st.columns([1, 1, 1])
col.title("Invest Dash")
col.title("")

with st.form("my_form"):
    username = st.text_input("Usuário", value=None)
    password = st.text_input("Senha", type="password", value=None)

    submitted = st.form_submit_button("Entrar")
    subscribe = st.form_submit_button("Cadastrar")
    if subscribe:
        st.switch_page("pages/4_cadastrar.py")
    if submitted:
        if username is not None and password is not None:
            is_authenticated, user, token = login(username, password)
            if is_authenticated:
                del user["password"]
                st.session_state["user"] = user
                st.session_state["token"] = token
                st.rerun()
            else:
                st.warning("Usuário ou senha inválido")
        else:
            st.warning("Usuário ou senha inválido")
