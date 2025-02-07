import mercadopago

# Token do Mercado Pago diretamente no código
token = "APP_USR-6731345204339065-020710-68737c81ae3389b9e045d69cbc904e8b-2255989128"

def gerar_link(servico, valor):
    sdk = mercadopago.SDK(token)

    payment_data = {
        "items": [
            {
                "id": "1",
                "title": servico,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 35
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
