import pandas as pd
import plotly_express as px
import streamlit as st


#Lendo as bases de dados
df_vendas = pd.read_excel('Datasets/Vendas.xlsx')
df_produtos = pd.read_excel('Datasets/Produtos.xlsx')

df = pd.merge(df_vendas,df_produtos,how='left',on='ID Produto')

# Novas colunas
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"] = df["Valor Venda"] - df["Custo"]
df['mes_ano'] = df['Data Venda'].dt.to_period("M").astype(str)

#Custo total
total_custo = (df['Custo'].sum().astype(str)).replace(".",",")
total_custo = "R$ " + total_custo[:2] + "." + total_custo[2:5] + "." + total_custo[5:]
#Lucro total
lucro = (round(df["Lucro"].sum(),2)).astype(str).replace(".",",")
lucro = "R$ " + lucro[:2] + "." + lucro[2:5] + "." + lucro[5:]

#Agrupamentos
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()

#Criando figura 
fig1 = px.bar(produtos_vendidos_marca, x='Quantidade', 
    y='Marca', orientation="h", text="Quantidade", 
    width=380, height=400, title="Total Produtos vendidos por Marca")

fig2 = px.pie(lucro_categoria, values='Lucro', names='Categoria',
    title="Lucro por Categoria",width=450, height=400 )

lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()
fig3 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", 
    title='Lucro X Mês X Categoria', width=900, height=400,
    markers=True, color="Categoria", 
              labels={"mes_ano":"Mês", "Lucro":"Lucro no Mês"})



def main():

    st.title("Análise de Vendas")
    st.image('vendas.png')
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Total Custo',total_custo)
    with col2:
        st.metric('Lucro', lucro)
    with col3:
        st.metric('Total Clientes',df['ID Cliente'].nunique())
    #Adiciona 2 gráficos lado a lado
    col1,col2 = st.columns(2)
    col1.plotly_chart(fig1)
    col2.plotly_chart(fig2)
    st.plotly_chart(fig3)


if __name__ == '__main__':
    main()

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )