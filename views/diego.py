import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades, buscar_senha_barbeiro, atualizar_senha_barbeiro
from datetime import datetime
import pandas as pd
import base64
import plotly.express as px

# Configuração da página
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
    barbeiro_selecionado = "diego"  # Fixo no diego

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
                id_barbeiro=2,
                barbeiro="diego",
                data_hora=data_hora,
                servico=servico_selecionado[1],
                valor=float(servico_selecionado[2]),
                observacao=observacao
            )
            st.success("Atividade cadastrada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao cadastrar atividade: {e}")

# Exibir atividades apenas do diego
st.markdown("---")
st.title("Atividades de diego 💈")

atividades = buscar_atividades()
if atividades:
    df = pd.DataFrame(atividades)

    # Filtrar apenas diego
    df = df[df["barbeiro"] == "diego"]

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

    st.markdown("---")
    st.title(f"💰 Acesso Financeiro - {barbeiro_selecionado.capitalize()}")

    senha_correta = buscar_senha_barbeiro(barbeiro_selecionado)  # Busca a senha no banco

    if senha_correta:
        senha_digitada = st.text_input("Digite sua senha para ver os valores:", type="password")

        if senha_digitada:
            if senha_digitada == senha_correta:
                st.success("✅ Acesso liberado!")

                # Exibir KPIs financeiros
                col1, col2 = st.columns(2)
                total_valor = df_filtrado["valor"].sum()
                col1.metric(label="💰 Receita Total no Período", value=f"R$ {total_valor:.2f}")

                lucro_percentual = col2.slider("Selecione o percentual de lucro:", min_value=10, max_value=100, value=50, step=5)
                lucro_calculado = (total_valor * lucro_percentual) / 100
                col2.metric(label=f"📈 Lucro Estimado ({lucro_percentual}%)", value=f"R$ {lucro_calculado:.2f}")

                # Criar gráfico de barras
                st.subheader("📊 Receita por Data")
                df_filtrado["Data"] = df_filtrado["data_hora"].dt.date
                fig = px.bar(df_filtrado, x="Data", y="valor", title="Receita por Data", labels={"Data": "Data", "valor": "Valor R$"}, text_auto=True)
                st.plotly_chart(fig, use_container_width=True)

                # Exibir DataFrame abaixo do gráfico
                st.subheader("📋 Atividades Registradas")
                st.dataframe(df_filtrado, use_container_width=True)

            else:
                st.error("❌ Senha incorreta! Tente novamente.")
        
        # Opção de troca de senha visível apenas se o usuário estiver logado
        if senha_digitada == senha_correta:
            st.subheader("🔒 Alterar Senha")

            # Campo para a nova senha
            nova_senha = st.text_input("Digite a nova senha:", type="password")
            confirmar_senha = st.text_input("Confirme a nova senha:", type="password")

            if st.button("Alterar Senha"):
                if nova_senha and confirmar_senha:
                    if nova_senha == confirmar_senha:
                        try:
                            atualizar_senha_barbeiro(barbeiro_selecionado, nova_senha)
                            st.success("Senha alterada com sucesso! 🎉")
                        except Exception as e:
                            st.error(f"Erro ao atualizar senha: {e}")
                    else:
                        st.error("As senhas não coincidem. Tente novamente.")
                else:
                    st.warning("Preencha os dois campos para trocar a senha.")

    else:
        # Se o barbeiro não souber a senha
        if st.button("Esqueci minha senha"):
            # Aqui pode-se adicionar a lógica para recuperação ou redefinição de senha
            st.warning("Para redefinir a senha, entre em contato com o administrador da plataforma.")

st.markdown("---")
