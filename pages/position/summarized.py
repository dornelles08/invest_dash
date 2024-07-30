import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.resume import resume
from pages.position.common import get_infos

infos = get_infos()

col1, col2 = st.columns([1, 1])


fig = go.Figure()

positive_infos = infos[infos["Ganho"] >= 0]
positive_infos = positive_infos.sort_values(by=["Ganho"], ascending=True)

negative_infos = infos[infos["Ganho"] < 0]
negative_infos = negative_infos.sort_values(by=["Ganho"], ascending=True)

fig.add_trace(
    go.Bar(y=negative_infos["Ativo"], x=negative_infos["Ganho"],
           orientation='h', marker_color="red"))
fig.add_trace(
    go.Bar(y=positive_infos["Ativo"], x=positive_infos["Ganho"],
           orientation='h', marker_color="green"))
fig.update_layout(showlegend=False)

col1.plotly_chart(fig, use_container_width=True)

resume_general = pd.DataFrame({
    "Total de Ativos": [infos["Ganho"].count()],
    "Ganhos Totais": [round(infos["Ganho"].sum(), 2)],
    "Ganhos Percentuais": [round(infos["% Ganho"].sum(), 2)],
})
col1.dataframe(data=resume_general,
               hide_index=True,
               column_config={
                   "Ganhos Percentuais": st.column_config.NumberColumn(format="%.2f %%"),
                   "Ganhos Totais": st.column_config.NumberColumn(format="R$ %.2f"),
               })

resume(infos, columns=[
    "Ativo",
    "Preço Atual",
    "Ganho",
    "% Ganho"
], display=col2)
