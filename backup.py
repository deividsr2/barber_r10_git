import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades
from datetime import datetime
import pandas as pd
import base64
import imghdr

# Configuração da página (DEVE SER A PRIMEIRA COISA NO SCRIPT)
st.set_page_config(page_title="R10 Barber Shop", page_icon=Image.open("logo.png"), layout="centered")

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
    barbeiro_selecionado = st.selectbox(
        "Barbeiro:",
        options=lista_barbeiros,
        format_func=lambda x: x[1]
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
            inserir_atividade(
                id_barbeiro=barbeiro_selecionado[0],
                barbeiro=barbeiro_selecionado[1],
                data_hora=data_hora,
                servico=servico_selecionado[1],
                valor=float(servico_selecionado[2]),
                observacao=observacao
            )
            st.success("Atividade cadastrada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao cadastrar atividade: {e}")

# Tabela de atividades
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

#teste do carrosel------------------------------------------------------------------------------------------------



# Função para converter imagem em base64



# Lista de nomes das imagens sem extensão
nomes_imagens = ["cleiton", "daniel", "diego", "juan", "randerson"]

# Detectar automaticamente a extensão das imagens
imagens = []
for nome in nomes_imagens:
    for ext in ["jpg", "jpeg", "png"]:
        caminho = f"{nome}.{ext}"
        try:
            with open(caminho, "rb") as f:
                if imghdr.what(f) in ["jpeg", "png"]:
                    imagens.append(caminho)
                    break
        except FileNotFoundError:
            continue

# Converter imagens para Base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        img_format = imghdr.what(img_file)
        return base64.b64encode(img_file.read()).decode(), img_format

# Lista de imagens em Base64
imagens_base64 = [get_image_base64(img) for img in imagens]

# Criando o carrossel com todas as 5 imagens visíveis
carousel_html = f"""
<style>
    .carousel-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        max-width: 1000px; /* Ajuste o tamanho conforme necessário */
        margin: auto;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    }}

    .carousel-slide {{
        display: flex;
        width: 100%;
        gap: 10px; /* Espaço entre as imagens */
    }}

    .carousel-slide img {{
        width: calc(100% / {len(imagens)});
        max-width: 200px;
        flex-shrink: 0;
        padding: 10px;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.3s, border 0.3s;
        border: 4px solid transparent;
    }}

    .carousel-slide img:hover {{
        transform: scale(1.1);
    }}

    .selected {{
        border: 4px solid #ffcc00 !important;
    }}
</style>

<div class="carousel-container">
    <div class="carousel-slide">
        {''.join(f'<img src="data:image/{fmt};base64,{b64}" onclick="selectImage(this)" alt="Imagem">' for b64, fmt in imagens_base64)}
    </div>
</div>

<script>
    function selectImage(img) {{
        document.querySelectorAll('.carousel-slide img').forEach(img => img.classList.remove('selected'));
        img.classList.add('selected');
    }}
</script>
"""

st.markdown(carousel_html, unsafe_allow_html=True)