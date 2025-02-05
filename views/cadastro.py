import streamlit as st
from banco import inserir_servico, buscar_servicos

# Título da página
st.title("Cadastro de Serviços")

# Formulário para inserir novos serviços
with st.form(key="servico_form"):
    servico = st.text_input("Nome do Serviço")
    valor = st.number_input("Valor do Serviço", min_value=0.0, step=0.01)
    submit_button = st.form_submit_button(label="Cadastrar Serviço")

# Quando o formulário for enviado
if submit_button:
    if servico and valor >= 0:
        # Inserir no banco de dados
        inserir_servico(servico, valor)
        st.success(f"Serviço '{servico}' cadastrado com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos corretamente.")

# Exibir lista de serviços cadastrados
st.subheader("Serviços Cadastrados")
servicos = buscar_servicos()
if servicos:
    for servico in servicos:
        st.write(f"{servico['id']}. {servico['servico']} - R${servico['valor']}")
else:
    st.warning("Nenhum serviço cadastrado ainda.")
