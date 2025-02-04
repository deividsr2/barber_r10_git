import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades
from datetime import datetime
import pandas as pd
import base64

# Configuração da página (DEVE SER A PRIMEIRA COISA NO SCRIPT)
# st.set_page_config(page_title="R10 Barber Shop", page_icon=Image.open("logo.png"), layout="centered")

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

st.title("Navegação entre Páginas")

# Menu de navegação
page = st.sidebar.selectbox(
    "Selecione a página:",
    ["Seleção de Barbeiros", "Cadastro de Atividades", "Cleiton", "Daniel", "Diego", "Juan", "Randerson"]
)

# Páginas
if page == "Seleção de Barbeiros":
    st.header("Seleção de Barbeiros")
    st.write("Navegue para a página dos barbeiros através do menu ao lado.")

elif page == "Cadastro de Atividades":
    st.header("Cadastro de Atividades")
    
    barbeiros = buscar_barbeiros()
    servicos = buscar_servicos()
    
    lista_barbeiros = [(barbeiro["id"], barbeiro["barbeiro"]) for barbeiro in barbeiros]
    lista_servicos = [(servico["id"], servico["servico"], servico["valor"]) for servico in servicos]
    
    st.subheader("Preencha os detalhes da atividade:")
    with st.form("form_atividade"):
        barbeiro_selecionado = st.selectbox(
            "Barbeiro:",
            [barbeiro[1] for barbeiro in lista_barbeiros]
        )
    
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
                barbeiro_id = next(barbeiro[0] for barbeiro in lista_barbeiros if barbeiro[1] == barbeiro_selecionado)
                inserir_atividade(
                    id_barbeiro=barbeiro_id,
                    barbeiro=barbeiro_selecionado,
                    data_hora=data_hora,
                    servico=servico_selecionado[1],
                    valor=float(servico_selecionado[2]),
                    observacao=observacao
                )
                st.success("Atividade cadastrada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao cadastrar atividade: {e}")

    st.subheader("Atividades Registradas")
    atividades = buscar_atividades()
    
    if atividades:
        df = pd.DataFrame(atividades)
        df.rename(
            columns={
                "id": "ID",
                "id_barbeiro": "ID Barbeiro",
                "barbeiro": "Barbeiro",
                "data_hora": "Data e Hora",
                "servico": "Serviço",
                "valor": "Valor",
                "observacao": "Observação",
            },
            inplace=True,
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma atividade registrada até o momento.")

elif page == "Cleiton":
    st.header("Cleiton")
    from views import cleiton
    cleiton.display()

elif page == "Daniel":
    st.header("Daniel")
    from views import daniel
    daniel.display()

elif page == "Diego":
    st.header("Diego")
    from views import diego
    diego.display()

elif page == "Juan":
    st.header("Juan")
    from views import juan
    juan.display()

elif page == "Randerson":
    st.header("Randerson")
    from views import randerson
    randerson.display()

else:
    st.error("Página não encontrada.")
