import streamlit as st

st.title("Bem-vindo à R10 Barber Shop")
st.write("Use o menu à esquerda para navegar entre as páginas dos barbeiros.")




# Código HTML, CSS e JavaScript para o carrossel
carousel_html = """
<style>
    .carousel {
        position: relative;
        width: 100%;
        max-width: 600px;
        margin: auto;
        overflow: hidden;
        border: 2px solid #ccc;
        border-radius: 10px;
    }
    .carousel img {
        width: 100%;
        display: none;
        border-radius: 10px;
    }
    .carousel img.active {
        display: block;
        animation: fade 1.5s;
    }
    @keyframes fade {
        from {opacity: 0.4;}
        to {opacity: 1;}
    }
    .carousel button {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        padding: 10px;
        cursor: pointer;
        border-radius: 50%;
    }
    .carousel button.prev {
        left: 10px;
    }
    .carousel button.next {
        right: 10px;
    }
</style>

<div class="carousel">
    <img src="cleiton.jpg" class="active">
    <img src="diego.jpg">
    <img src="daniel.jpg">
    <img src="juan.jpg">
    <img src="randerson.jpg">
    <button class="prev" onclick="prevSlide()">&#10094;</button>
    <button class="next" onclick="nextSlide()">&#10095;</button>
</div>

<script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel img');

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
            }
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }

    // Auto-play (opcional)
    setInterval(nextSlide, 3000); // Muda de slide a cada 3 segundos
</script>
"""

# Exibe o carrossel no Streamlit
st.components.v1.html(carousel_html)