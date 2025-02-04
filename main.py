import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades
from datetime import datetime
import pandas as pd
import base64

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






# --- PAGE SETUP ---
Home = st.Page(
    "views/home.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)
cleiton = st.Page(
    "views/cleiton.py",
    title="cleiton ",
    icon=":material/bar_chart:",
)
diego = st.Page(
    "views/diego.py",
    title="diego",
    icon=":material/smart_toy:",
)
daniel = st.Page(
    "views/daniel.py",
    title="daniel",
    icon=":material/smart_toy:",
)
juan = st.Page(
    "views/juan.py",
    title="juan",
    icon=":material/smart_toy:",
)
randerson = st.Page(
    "views/randerson.py",
    title="randerson",
    icon=":material/smart_toy:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Home": [Home],
        "Barbeiros": [cleiton,daniel,diego,juan,randerson],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("logo.png")



# --- RUN NAVIGATION ---
pg.run()
