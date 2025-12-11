import streamlit as st
import pandas as pd
import base64

# Injection du lien de la police 'Great Vibes' via <link>
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)


# -- Chargement fichier CSS
with open("assets/style.css", encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# ----------------------------------------------------------------------

# -- Création de l'arrière plan
# Convertir l'image en Base64
with open ("images/Gemini_Generated_Image_fond.png","rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# Mise en page directement dans st.markdown (sans passer par CSS)
st.markdown(f"""
    <style>
    body {{
        background-image: url("data:image/png;base64,{encoded}");
    }}
    </style>
    """, unsafe_allow_html=True)



# -- Titre page
st.markdown(f"""
    <h1 class="title">
        Le site de recommandations ciblé et pertinent
    </h1>
    """, unsafe_allow_html=True)


# -- Création des colonnes FILMS
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

actors = """
<div class="right-container">
    <img src="https://static.streamlit.io/examples/cat.jpg" class="image1-top-left">
    <img src="https://static.streamlit.io/examples/dog.jpg" class="image2-top-middle">
    <img src="https://static.streamlit.io/examples/owl.jpg" class="image3-top-right">
</div>
"""
st.markdown(actors, unsafe_allow_html=True)


# Pour le champ recherche avec loupe
# --- 1. Définition du Style CSS ---


# --- 3. WIDGET DE SAISIE DE TEXTE ---
recherche_film = st.text_input(
    label="", # Label vide, géré par le CSS
    placeholder="Rentrez le nom d'un film...",
    key="search_input"
)

# Affichage du résultat pour vérifier
if recherche_film:
    st.info(f"Recherche lancée pour : **{recherche_film}**")


