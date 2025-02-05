import streamlit as st
from banco import buscar_atividades
import pandas as pd
import base64
import plotly.express as px

# Configuração da página

# Função para definir o background
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    
    background_style = f"""
    <style>
    .stApp {{
        background: url(data:image/jpg;base64,{encoded_string}) no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Chama a função para definir o fundo
set_background("bc.jpg")

st.title("📊 Painel Financeiro")

# Buscar todas as atividades (de todos os barbeiros)
atividades = buscar_atividades()

if atividades:
    df = pd.DataFrame(atividades)

    # Converter 'data_hora' para datetime
    df["data_hora"] = pd.to_datetime(df["data_hora"], format="%Y-%m-%d %H:%M:%S")

    # Criar filtro de data ACIMA DOS GRÁFICOS
    st.subheader("📅 Filtro de Data")
    col1, col2 = st.columns(2)

    data_min = df["data_hora"].min().date()
    data_max = df["data_hora"].max().date()
    
    data_inicio = col1.date_input("Data inicial:", data_min)
    data_fim = col2.date_input("Data final:", data_max)

    # Aplicar filtro de data
    df_filtrado = df[(df["data_hora"].dt.date >= data_inicio) & (df["data_hora"].dt.date <= data_fim)]

    # Criar KPIs acima dos gráficos
    col1, col2, col3 = st.columns(3)

    total_valor = df_filtrado["valor"].sum()
    col1.metric(label="💰 Receita Total", value=f"R$ {total_valor:.2f}")

    lucro_percentual = col2.slider("Selecione o percentual de lucro:", min_value=10, max_value=100, value=50, step=5)
    lucro_calculado = (total_valor * lucro_percentual) / 100
    col2.metric(label=f"📈 Lucro Estimado ({lucro_percentual}%)", value=f"R$ {lucro_calculado:.2f}")

    total_servicos = df_filtrado.shape[0]
    col3.metric(label="💼 Serviços Realizados", value=f"{total_servicos}")

    # 📊 Gráfico de barras - Receita por Data
    st.subheader("📊 Receita por Data")
    df_filtrado["Data"] = df_filtrado["data_hora"].dt.date  # Removendo a hora do eixo X
    fig1 = px.bar(
        df_filtrado,
        x="Data",
        y="valor",
        title="Receita por Data",
        labels={"Data": "Data", "valor": "Valor R$"},
        text_auto=True
    )



    st.plotly_chart(fig1, use_container_width=True)

    # 📊 Gráfico de pizza - Receita por Barbeiro
    st.subheader("🍕 Receita por Barbeiro")
    fig2 = px.pie(
        df_filtrado,
        names="barbeiro",
        values="valor",
        title="Faturamento por Barbeiro",
        hole=0.4  # Para estilo de donut
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 📊 Gráfico de barras - Receita por Tipo de Serviço
    st.subheader("💇‍♂️ Receita por Tipo de Serviço")
    fig3 = px.bar(
        df_filtrado,
        x="servico",
        y="valor",
        title="Faturamento por Tipo de Serviço",
        labels={"servico": "Serviço", "valor": "Valor R$"},
        text_auto=True,
        color="servico"
    )

    

    st.plotly_chart(fig3, use_container_width=True)

    # Exibir DataFrame abaixo dos gráficos
    st.subheader("📋 Atividades Registradas")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.info("Nenhuma atividade registrada até o momento.")
