import streamlit as st
from PIL import Image
import base64
import os

# Configuração da página
st.set_page_config(page_title="R10 Barber Shop", page_icon="logo.png", layout="centered")

# Função para converter imagem em Base64 (para incorporar no HTML)
def img_to_base64(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    return base64.b64encode(img_bytes).decode()

# Lista de barbeiros e possíveis extensões de imagem
barber_names = ["cleiton", "daniel", "diego", "juan", "randerson"]
extensions = ["jpg", "jpeg", "png"]

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

# Depuração: exibe os query params atuais
st.write("Query Parameters:", st.query_params)

# Inicializa ou atualiza o estado da sessão para a página (view) selecionada
if "page" not in st.session_state:
    st.session_state["page"] = ""

query_params = st.query_params
if "page" in query_params:
    # Se o valor for uma lista, pegue o primeiro elemento; caso contrário, use-o diretamente.
    value = query_params["page"]
    if isinstance(value, list):
        st.session_state["page"] = value[0]
    else:
        st.session_state["page"] = value
else:
    st.session_state["page"] = ""

st.write("Página selecionada (state):", st.session_state["page"])

# Se nenhum parâmetro "page" for definido, exibe a tela de navegação com as imagens
if st.session_state["page"] == "":
    st.title("Selecione um Barbeiro")
    st.markdown("Clique na imagem para navegar para a página do barbeiro.")

    # Criar o carrossel de imagens
    carousel_html = """
    <style>
        .carousel {{
            display: flex;
            overflow: hidden;
            width: 100%;
        }}
        .carousel img {{
            flex: 1;
            transition: transform 0.5s ease;
            max-width: 100%;
            height: auto;
        }}
        .carousel-container {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .carousel-button {{
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            border: none;
            padding: 10px;
            cursor: pointer;
            font-size: 18px;
            margin: 0 10px;
        }}
    </style>
    <div class="carousel-container">
        <button class="carousel-button" onclick="prevSlide()">&#10094;</button>
        <div class="carousel" id="carousel">
            {''.join(f'<img src="data:image/{{ext}};base64,{img_to_base64(f"{barber}.{ext}")}" alt="{barber.title()}">' for barber in barber_names for ext in extensions if os.path.exists(f"{barber}.{ext}"))}
        </div>
        <button class="carousel-button" onclick="nextSlide()">&#10095;</button>
    </div>
    <script>
        let currentIndex = 0;
        const slides = document.querySelectorAll('.carousel img');
        const totalSlides = slides.length;

        function updateSlidePosition() {{
            slides.forEach((slide, index) => {{
                slide.style.transform = `translateX(${{(index - currentIndex) * 100}}%)`;
            }});
        }}

        function nextSlide() {{
            currentIndex = (currentIndex + 1) % totalSlides;
            updateSlidePosition();
        }}

        function prevSlide() {{
            currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
            updateSlidePosition();
        }}

        updateSlidePosition(); // Initialize position
    </script>
    """

    st.markdown(carousel_html, unsafe_allow_html=True)

# Se o parâmetro "page" estiver definido, carrega a view correspondente
else:
    page = st.session_state["page"]

    # Botão para voltar à página inicial (limpa o parâmetro "page")
    if st.sidebar.button("Voltar"):
        st.query_params(page="")

    st.write("Carregando view para:", page)
    
    if page == "cleiton":
        from views import cleiton
    elif page == "daniel":
        from views import daniel
    elif page == "diego":
        from views import diego
    elif page == "juan":
        from views import juan
    elif page == "randerson":
        from views import randerson
    else:
        st.error("Barbeiro não encontrado.")
