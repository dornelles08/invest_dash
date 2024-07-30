import pandas as pd
import streamlit as st

from components.resume import resume
from pages.position.common import get_infos

infos = get_infos()

resume(infos, columns=[
    "Ativo",
    "Segmento",
    "Tipo",
    "Quantidade",
    "Preço Médio",
    "Valor Investido",
    "Preço Atual",
    "Saldo",
    "Ganho",
    "% Ganho",
    "P/VP",
    "Percentual",
    "Categoria"
])

resume_general = pd.DataFrame({
    "Total de Ativos": [infos["Ganho"].count()],
    "Ganhos Totais": [round(infos["Ganho"].sum(), 2)],
    "Ganhos Percentuais": [round(infos["% Ganho"].sum(), 2)],
})
st.dataframe(data=resume_general,
             hide_index=True,
             column_config={
                 "Ganhos Percentuais": st.column_config.NumberColumn(format="%.2f %%"),
                 "Ganhos Totais": st.column_config.NumberColumn(format="R$ %.2f"),
             })
