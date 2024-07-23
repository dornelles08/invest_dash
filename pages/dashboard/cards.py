from datetime import datetime

import streamlit as st

from functions.load_data import get_fiis_infos
from services.dados import DadosService
from services.user import UserService


def cards(infos):
    """ 
      Função responsavel por exibir cards de 
        Valor Aplicado, Saldo Bruto, Valorização
    """
    dados_service = DadosService()
    user_services = UserService()

    investido = round(infos["Valor Investido"].sum(), 2)

    saldo_total = round(infos["Saldo"].sum(), 2)

    variation_percentual = round(((saldo_total/investido)-1)*100, 2)

    variation = round((saldo_total-investido), 2)

    col1, col2, col3, _, col = st.columns(
        [3, 3, 3, 4, 3], vertical_alignment="bottom")
    col1.metric(label="Valor Aplicado",
                value=f"R$ {investido}")
    col2.metric(label="Valor Atual",
                value=f"R$ {saldo_total}")
    col3.metric(label="Valorização",
                value=f"R$ {variation}",
                delta=f"{variation_percentual} %")

    if col.button("Atualizar Base"):
        user_sync = datetime.strptime(
            st.session_state["user"]["sync"], "%x %X")
        if (user_sync - datetime.now()).seconds >= 900:
            fiis_infos = get_fiis_infos(
                st, st.session_state["user"]["_id"])
            dados_service.upsert_dados(fiis_infos)
            user_services.update_user({
                **st.session_state["user"],
                "sync": datetime.now().strftime("%x %X")
            })
        st.session_state["dados"] = None
        st.success("Transação Adicionada com Sucesso", icon="✅")
        st.rerun()
