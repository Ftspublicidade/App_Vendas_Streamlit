import pandas as pd
import streamlit as st
import numpy as np

@st.cache_data
def carregar_dados():
    # carregar as bases de dados
    df_vendas = pd.read_excel("Vendas.xlsx")
    df_produtos = pd.read_excel("Produtos.xlsx")

    df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto')

    # Criando colunas
    df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
    df["Lucro"] = df["Valor Venda"] - df["Custo"]
    df["mes_ano"] = df["Data Venda"].dt.to_period("M").astype(str)
    df["Ano"] = df["Data Venda"].dt.year

    return df



def color_negative(valor):
    color = "red" if valor < 0 else "black"
    return f'color: {color}'

def main():

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