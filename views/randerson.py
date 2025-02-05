import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades
from datetime import datetime
import pandas as pd
import base64
import plotly.express as px

# Configuração da página
#st.set_page_config(page_title="R10 Barber Shop", page_icon="💈", layout="centered")

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

with st.container():
    col1, col2 = st.columns([1, 4])
    logo = Image.open("logo.png")
    col1.image(logo, width=150)
    col2.title("R10 Barber Shop")

st.markdown("---")
st.title("Cadastro de Atividades")

# Buscar dados das tabelas r10_barbeiros e r10_servicos
barbeiros = buscar_barbeiros()
servicos = buscar_servicos()

# Montar listas para os selectbox
lista_barbeiros = [(barbeiro["id"], barbeiro["barbeiro"]) for barbeiro in barbeiros]
lista_servicos = [(servico["id"], servico["servico"], servico["valor"]) for servico in servicos]

# Formulário para cadastro de atividades
st.subheader("Preencha os detalhes da atividade:")
with st.form("form_atividade"):
    barbeiro_selecionado = "randerson"  # Fixo no randerson

    servico_selecionado = st.selectbox(
        "Serviço:",
        options=lista_servicos,
        format_func=lambda x: f"{x[1]} - R$ {x[2]:.2f}"
    )

    observacao = st.text_area("Observação (opcional):")

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    submitted = st.form_submit_button("Cadastrar Atividade")

    if submitted:
        try:
            inserir_atividade(
                id_barbeiro=3,
                barbeiro="randerson",
                data_hora=data_hora,
                servico=servico_selecionado[1],
                valor=float(servico_selecionado[2]),
                observacao=observacao
            )
            st.success("Atividade cadastrada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao cadastrar atividade: {e}")

# Exibir atividades apenas do randerson
st.markdown("---")
st.title("Atividades de randerson 💈")

atividades = buscar_atividades()
if atividades:
    df = pd.DataFrame(atividades)
    
    # Filtrar apenas randerson
    df = df[df["barbeiro"] == "randerson"]

    # Converter 'data_hora' para datetime
    df["data_hora"] = pd.to_datetime(df["data_hora"], format="%Y-%m-%d %H:%M:%S")

    # Criar filtro de data ACIMA DO GRÁFICO
    st.subheader("📅 Filtro de Data")
    col1, col2 = st.columns(2)

    data_min = df["data_hora"].min().date()
    data_max = df["data_hora"].max().date()
    
    data_inicio = col1.date_input("Data inicial:", data_min)
    data_fim = col2.date_input("Data final:", data_max)

    # Aplicar filtro de data
    df_filtrado = df[(df["data_hora"].dt.date >= data_inicio) & (df["data_hora"].dt.date <= data_fim)]

    # Exibir KPI acima do gráfico com cálculo de lucro
    col1, col2 = st.columns(2)
    
    total_valor = df_filtrado["valor"].sum()
    col1.metric(label="💰 Receita Total no Período", value=f"R$ {total_valor:.2f}")

    lucro_percentual = col2.slider("Selecione o percentual de lucro:", min_value=10, max_value=100, value=50, step=5)
    lucro_calculado = (total_valor * lucro_percentual) / 100
    col2.metric(label=f"📈 Lucro Estimado ({lucro_percentual}%)", value=f"R$ {lucro_calculado:.2f}")

    # Criar gráfico de barras sem background
    st.subheader("📊 Receita por Data")
    df_filtrado["Data"] = df_filtrado["data_hora"].dt.date  # Removendo a hora do eixo X
    fig = px.bar(
        df_filtrado,
        x="Data",  # Agora apenas a data, sem hora
        y="valor",
        title="Receita por Data",
        labels={"Data": "Data", "valor": "Valor R$"},
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)


    # Exibir DataFrame abaixo do gráfico
    st.subheader("📋 Atividades Registradas")
    st.dataframe(df_filtrado, use_container_width=True)
else:
    st.info("Nenhuma atividade registrada até o momento.")
