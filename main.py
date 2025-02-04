import streamlit as st
from PIL import Image
import base64

# Configuração da página
st.set_page_config(page_title="R10 Barber Shop", page_icon="logo.png", layout="centered")

# Função para converter imagem em Base64 (para incorporar no HTML)
def img_to_base64(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    return base64.b64encode(img_bytes).decode()

# Exibe o background e o logo
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

with st.container():
    col1, col2 = st.columns([1, 4])
    logo = Image.open("logo.png")
    col1.image(logo, width=150)
    col2.title("R10 Barber Shop")

st.markdown("---")

# Inicializa ou atualiza o estado da sessão para a página (view) selecionada
if "page" not in st.session_state:
    st.session_state["page"] = ""

# Exibe a lista de barbeiros para navegação
barber_names = ["cleiton", "daniel", "diego", "juan", "randerson"]

if st.session_state["page"] == "":
    st.title("Selecione um Barbeiro")
    for barber in barber_names:
        if st.button(barber.title()):
            st.session_state["page"] = barber

# Se o parâmetro "page" estiver definido, carrega a view correspondente
else:
    page = st.session_state["page"]
    
    # Botão para voltar à página inicial
    if st.sidebar.button("Voltar"):
        st.session_state["page"] = ""

    st.write(f"Carregando view para: {page}")
    
    if page == "cleiton":
        st.write("Conteúdo do Cleiton")
        # from views import cleiton
    elif page == "daniel":
        st.write("Conteúdo do Daniel")
        # from views import daniel
    elif page == "diego":
        st.write("Conteúdo do Diego")
        # from views import diego
    elif page == "juan":
        st.write("Conteúdo do Juan")
        # from views import juan
    elif page == "randerson":
        st.write("Conteúdo do Randerson")
        # from views import randerson
    else:
        st.error("Barbeiro não encontrado.")
