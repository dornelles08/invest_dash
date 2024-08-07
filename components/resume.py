import streamlit as st


def resume(infos,
           columns=["Ativo", "Quantidade", "Preço Médio", "Valor Investido",
                    "Preço Atual", "Saldo", "% Ganho", "Ganho", "Percentual"],
           display=None):
    if display is None:
        display = st

    df = infos[columns]
    display.dataframe(
        data=df,
        hide_index=True,
        height=500,
        use_container_width=True,
        column_config={
            "Preço Atual": st.column_config.NumberColumn(format="R$ %.2f"),
            "Preço Médio": st.column_config.NumberColumn(format="R$ %.2f"),
            "Saldo": st.column_config.NumberColumn(format="R$ %.2f"),
            "Percentual": st.column_config.NumberColumn(format="%.2f %%"),
            "% Ganho": st.column_config.NumberColumn(format="%.2f %%"),
            "Ganho": st.column_config.NumberColumn(format="R$ %.2f"),
            "Valor Investido": st.column_config.NumberColumn(format="R$ %.2f"),
        }
    )
