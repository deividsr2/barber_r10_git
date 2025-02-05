import streamlit as st
import base64

# Título da página
st.title("Bem-vindo à R10 Barber Shop")
st.write("Use o menu à esquerda para navegar entre as páginas dos barbeiros.")

# Lista de imagens e links correspondentes
imagens_links = {
    "cleiton.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/cleiton",
    "diego.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/diego",
    "daniel.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/daniel",
    "juan.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/juan",
    "randerson.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/randerson",
}

# Função para converter imagens em Base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Gerar imagens com links em Base64 para embutir no HTML
image_tags = "".join(
    [
        f'<a href="{link}" target="_blank"><img src="data:image/jpg;base64,{get_image_base64(img)}" class="{"active" if i == 0 else ""}"></a>'
        for i, (img, link) in enumerate(imagens_links.items())
    ]
)

# Código HTML do carrossel
carousel_html = f"""
<style>
    .carousel {{
        position: relative;
        width: 100%;
        max-width: 600px;
        margin: auto;
        overflow: hidden;
        border-radius: 10px;
    }}
    .carousel img {{
        width: 100%;
        display: none;
        border-radius: 10px;
    }}
    .carousel img.active {{
        display: block;
        animation: fade 1.5s;
    }}
    @keyframes fade {{
        from {{opacity: 0.4;}}
        to {{opacity: 1;}}
    }}
    .carousel button {{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        padding: 10px;
        cursor: pointer;
        border-radius: 50%;
        font-size: 18px;
    }}
    .carousel button.prev {{
        left: 10px;
    }}
    .carousel button.next {{
        right: 10px;
    }}
</style>

<div class="carousel">
    {image_tags}
    <button class="prev" onclick="prevSlide()">&#10094;</button>
    <button class="next" onclick="nextSlide()">&#10095;</button>
</div>

<script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel a img');

    function showSlide(index) {{
        slides.forEach((slide, i) => {{
            slide.classList.remove('active');
            if (i === index) {{
                slide.classList.add('active');
            }}
        }});
    }}

    function nextSlide() {{
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }}

    function prevSlide() {{
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }}

    // Auto-play (muda de slide a cada 3 segundos)
    setInterval(nextSlide, 3000);
</script>
"""

# Exibir carrossel no Streamlit
st.components.v1.html(carousel_html, height=150)
