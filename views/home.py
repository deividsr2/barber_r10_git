import streamlit as st

st.title("Bem-vindo à R10 Barber Shop")
st.write("Use o menu à esquerda para navegar entre as páginas dos barbeiros.")



# HTML do carrossel
carousel_html = """
<html>
<head>
    <style>
        .carousel {
            position: relative;
            max-width: 600px;
            margin: auto;
            overflow: hidden;
            border-radius: 10px;
        }
        .carousel img {
            width: 100%;
            display: none;
        }
        .carousel img.active {
            display: block;
        }
        .prev, .next {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background-color: rgba(0,0,0,0.5);
            color: white;
            border: none;
            padding: 10px;
            cursor: pointer;
        }
        .prev { left: 10px; }
        .next { right: 10px; }
    </style>
</head>
<body>
    <div class="carousel">
        <img src="cleiton.jpg" class="active">
        <img src="diego.jpg">
        <img src="daniel.jpg">
        <img src="juan.jpg">
        <img src="randerson.jpg">
        <button class="prev" onclick="moveSlide(-1)">&#10094;</button>
        <button class="next" onclick="moveSlide(1)">&#10095;</button>
    </div>
    <script>
        let index = 0;
        const images = document.querySelectorAll('.carousel img');

        function moveSlide(step) {
            images[index].classList.remove('active');
            index = (index + step + images.length) % images.length;
            images[index].classList.add('active');
        }
    </script>
</body>
</html>
"""

# Renderizar o carrossel no Streamlit
st.components.v1.html(carousel_html, height=400)
