import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades, buscar_senha_barbeiro
from datetime import datetime
import pandas as pd
import base64
import plotly.express as px
import mercadopago
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Função para gerar link de pagamento
def gerar_link(servico, valor):
    sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_TOKEN"))

    payment_data = {
        "items": [
            {
                "id": "1",
                "title": servico,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor
            }
        ],
        "back_urls": {
            "success": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/sucesso",
            "failure": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/falha",
            "pending": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/falha"
        },
        "auto_return": "all"
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_pagamento = payment.get("init_point", "")

    return link_pagamento

# Definir fundo da página
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

set_background("bc.jpg")

# Cabeçalho da página
with st.container():
    col1, col2 = st.columns([1, 4])
    logo = Image.open("logo.png")
    col1.image(logo, width=150)
    col2.title("R10 Barber Shop")

st.markdown("---")
st.title("Cadastro de Atividades")

# Buscar barbeiros e serviços
barbeiros = buscar_barbeiros()
servicos = buscar_servicos()

lista_barbeiros = [(barbeiro["id"], barbeiro["barbeiro"]) for barbeiro in barbeiros]
lista_servicos = [(servico["id"], servico["servico"], servico["valor"]) for servico in servicos]

# Formulário para cadastro de atividades
st.subheader("Preencha os detalhes da atividade:")
with st.form("form_atividade"):
    barbeiro_selecionado = "cleiton"  # Fixo no Cleiton

    servico_selecionado = st.selectbox(
        "Serviço:",
        options=lista_servicos,
        format_func=lambda x: f"{x[1]} - R$ {x[2]:.2f}"
    )

    observacao = st.text_area("Observação (opcional):")

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    col1, col2 = st.columns(2)

    with col1:
        submitted = st.form_submit_button("Gerar Atividade ✂️")

    with col2:
        pagamento = st.form_submit_button("Ir para Pagamento 💳")

    if submitted:
        try:
            inserir_atividade(
                id_barbeiro=3,
                barbeiro="cleiton",
                data_hora=data_hora,
                servico=servico_selecionado[1],
                valor=float(servico_selecionado[2]),
                observacao=observacao
            )
            st.success("Atividade cadastrada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao cadastrar atividade: {e}")

    if pagamento:
        titulo_servico = servico_selecionado[1]
        valor_servico = float(servico_selecionado[2])  # Garantir que seja float
        link_pagamento = gerar_link(titulo_servico, valor_servico)
        
        if link_pagamento:
            st.success("✅ Link de pagamento gerado com sucesso!")
            st.markdown(f"[🔗 Clique aqui para pagar]({link_pagamento})", unsafe_allow_html=True)
        else:
            st.error("❌ Erro ao gerar link de pagamento. Tente novamente.")

# Exibir atividades apenas do Cleiton
st.markdown("---")
st.title("Atividades de Cleiton 💈")

atividades = buscar_atividades()
if atividades:
    df = pd.DataFrame(atividades)

    df = df[df["barbeiro"] == "cleiton"]

    df["data_hora"] = pd.to_datetime(df["data_hora"], format="%Y-%m-%d %H:%M:%S")

    st.subheader("📅 Filtro de Data")
    col1, col2 = st.columns(2)

    data_min = df["data_hora"].min().date()
    data_max = df["data_hora"].max().date()

    data_inicio = col1.date_input("Data inicial:", data_min)
    data_fim = col2.date_input("Data final:", data_max)

    df_filtrado = df[(df["data_hora"].dt.date >= data_inicio) & (df["data_hora"].dt.date <= data_fim)]

    st.markdown("---")
    st.title(f"💰 Acesso Financeiro - {barbeiro_selecionado.capitalize()}")

    senha_correta = buscar_senha_barbeiro(barbeiro_selecionado)

    if senha_correta:
        senha_digitada = st.text_input("Digite sua senha para ver os valores:", type="password")

        if senha_digitada:
            if senha_digitada == senha_correta:
                st.success("✅ Acesso liberado!")

                col1, col2 = st.columns(2)
                total_valor = df_filtrado["valor"].sum()
                col1.metric(label="💰 Receita Total no Período", value=f"R$ {total_valor:.2f}")

                lucro_percentual = col2.slider("Selecione o percentual de lucro:", min_value=10, max_value=100, value=50, step=5)
                lucro_calculado = (total_valor * lucro_percentual) / 100
                col2.metric(label=f"📈 Lucro Estimado ({lucro_percentual}%)", value=f"R$ {lucro_calculado:.2f}")

                st.subheader("📊 Receita por Data")
                df_filtrado["Data"] = df_filtrado["data_hora"].dt.date
                fig = px.bar(df_filtrado, x="Data", y="valor", title="Receita por Data", labels={"Data": "Data", "valor": "Valor R$"}, text_auto=True)
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📋 Atividades Registradas")
                st.dataframe(df_filtrado, use_container_width=True)
