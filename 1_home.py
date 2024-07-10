import streamlit as st

from functions.login import login, valid_token

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
                st.switch_page("pages/2_dashboard.py")
            else:
                st.warning("Usuário ou senha inválido")
        else:
            st.warning("Usuário ou senha inválido")
