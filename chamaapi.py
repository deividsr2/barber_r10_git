import streamlit as st
from api import gerar_link

st.title("Pagamento")

# Gerar o link de pagamento
link_pagamento = gerar_link()

# Exibir o botão
if st.button("Pagar agora 💳"):
    st.markdown(f"[Clique aqui para pagar]({link_pagamento})", unsafe_allow_html=True)

