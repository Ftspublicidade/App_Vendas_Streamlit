import pandas as pd
import streamlit as st
import numpy as np

@st.cache_data
def carregar_dados():
    
    df = pd.read_excel("Vendas.xlsx")

    return df



def color_negative(valor):
    color = "red" if valor < 0 else "black"
    return f'color: {color}'

def main():

    st.set_page_config(layout ="wide")

    df = carregar_dados()

    MoM = df.groupby("mes_ano")["Lucro"].sum().reset_index()
    MoM["Último Mês"] = MoM["Lucro"].shift(1)
    MoM["Variação"] = MoM["Lucro"] - MoM["Último Mês"]
    MoM["Variação%"] = MoM["Variação"] / MoM["Último Mês"] *100
    MoM["Variação%"] = MoM["Variação%"].map('{:.2f}%'.format)
    MoM["Variação%"] = MoM["Variação%"].replace("nan%", "")


    st.header("Análise Mensal")
    # Aplicando a função color_negative usando applymap
    df_styled = MoM.style.format({"Lucro": "R${:20,.2f}", 
                          "Lucro_LM": "R${:20,.2f}", 
                          "Variação": "{:20,.2f}"})\
                 .hide(axis="index")\
                 .applymap(color_negative, subset=["Variação"])

    st.dataframe(df_styled)
    





if __name__ == "__main__":
    main()