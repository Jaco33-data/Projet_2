import streamlit as st
import pandas as pd
import base64


# ----------------------------------------------------------------------
# --- Machine Learning





# --- POLICE GREAT VIBES
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- CSS GLOBAL
with open("assets/style.css", encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- FOND D'ÉCRAN
with open("images/Gemini_Generated_Image_fond.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    body {{
        background-image: url("data:image/png;base64,{encoded}");
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# --- IMAGES FILMS (GAUCHE)
films = """
<div class="left-container">
    <img src="https://static.streamlit.io/examples/cat.jpg" class="col1-top-left">
    <img src="https://static.streamlit.io/examples/dog.jpg" class="col2-top-middle">
    <img src="https://static.streamlit.io/examples/owl.jpg" class="col3-top-right">
    <img src="https://static.streamlit.io/examples/cat.jpg" class="col4-bottom-left">
    <img src="https://static.streamlit.io/examples/dog.jpg" class="col5-bottom-middle">
</div>
"""
st.markdown(films, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- IMAGES ACTEURS (DROITE)
actors = """
<div class="right-container">
    <img src="https://static.streamlit.io/examples/cat.jpg" class="image1-top-left">
    <img src="https://static.streamlit.io/examples/dog.jpg" class="image2-top-middle">
    <img src="https://static.streamlit.io/examples/owl.jpg" class="image3-top-right">
</div>
"""
st.markdown(actors, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- TITRE
st.markdown(
    """
    <h1 class="title">Le site de recommandations ciblé et pertinent</h1>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# --- VIGNETTE "FILMS"
st.markdown("""
<div class="film-badge">
    Films
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- VIGNETTE "ACTORS"
st.markdown("""
<div class="actor-badge">
    Acteurs
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- VIDÉO BANDE-ANNONCE
with st.container():
    col_gauche, col_centre, col_droite = st.columns([1, 4, 1])
    with col_centre:
        st.video("https://www.youtube.com/watch?v=M7lcd68a9HQ")

# ----------------------------------------------------------------------
# --- BOUTON SYNOPSIS
with st.container():
    col1, col_btn, col3 = st.columns([2, 1, 2])
    with col_btn:
        if st.button("Synopsis"):
            st.markdown(
                """
                <div style='text-align: center; font-size: 20px;'>
                Voici le résumé du film !
                </div>
                """,
                unsafe_allow_html=True
            )

# ----------------------------------------------------------------------
# --- BARRE DE RECHERCHE
st.text_input("Rentrez le nom d'un film...", label_visibility="collapsed")