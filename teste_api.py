 from openai import OpenAI

# # Configurações da API
# API_KEY = "sk-0e01301139534bee8185489b139264f5"  # Substitua pela sua chave de API da DeepSeek
# BASE_URL = "https://api.deepseek.com"  # URL base da API da DeepSeek

# # Inicializa o cliente da OpenAI configurado para a DeepSeek
# client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# # Função para enviar mensagem para a API da DeepSeek
# def enviar_mensagem(mensagem):
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": mensagem},
#         ],
#         stream=False
#     )
#     return response.choices[0].message.content

# # Configuração da interface do Streamlit
# st.title("Chat com DeepSeek API")

# # Inicializa o histórico de mensagens na sessão
# if 'historico' not in st.session_state:
#     st.session_state['historico'] = []

# # Entrada de texto do usuário
# user_input = st.text_input("Você:", "")

# # Botão para enviar a mensagem
# if st.button("Enviar"):
#     if user_input:
#         # Adiciona a mensagem do usuário ao histórico
#         st.session_state['historico'].append(f"Você: {user_input}")

#         # Envia a mensagem para a API e obtém a resposta
#         resposta = enviar_mensagem(user_input)

#         # Adiciona a resposta da API ao histórico
#         st.session_state['historico'].append(f"Bot: {resposta}")

# # Exibe o histórico de mensagens
# for mensagem in st.session_state['historico']:
#     st.text(mensagem)