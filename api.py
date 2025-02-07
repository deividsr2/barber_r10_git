import mercadopago
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def gerar_link(servico, valor):
    # Obter o token de acesso da variável de ambiente
    sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_TOKEN"))

    payment_data = {
        "items": [
            {
                "id": "1",
                "title": servico,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(valor)  # Convertendo para float antes de enviar
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
