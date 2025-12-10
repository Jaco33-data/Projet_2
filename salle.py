import streamlit as st
import pandas as pd
import base64

# -- Chargement fichier CSS
with open("assets/style.css") as f:
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
        Le site de recommandations ciblées et pertinentes
    </h1>
    """, unsafe_allow_html=True)

# Définir les genres et leurs icônes
#genres = {"Comédie": "😂","Drame": "😢", "Documentaire": "🎥"}

# Affichage
#for genre, icone in genres.items():
    #st.markdown(f'<div style="display:flex; gap:30px; margin-top:10px;color:white; font-size:20px;">{icone} {genre}</span>', unsafe_allow_html=True)


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
# Ce bloc de code définit le style visuel de la barre de recherche.
custom_css = """
<style>
/* Conteneur parent pour centrer la barre */
body {
    background-color: #fff;
    margin: 0;
    padding: 0;
}

/* Conteneur principal (La barre elle-même) */
div[class^="stTextInput"] > div {
    background-color: #FDF5E6;
    border-radius: 30px;
    border: 5px solid #D0A372;
    padding: 0px 50px 0px 10px;                 /* espace pour la loupe */
    box-shadow: 0 0 30px 20px rgba(255, 240, 200, 0.7);
    position: relative;
    height: 50px;
    width: 400px;                               /* largeur réduite */
    display: flex;
    align-items: center;
    margin-top: 5px;                            /* réduit l'espace vertical */
}

/* Champ <input> arrondi */
div[class^="stTextInput"] input {
    background-color: #FDF5E6 !important;
    box-shadow: 0 0 30px 20px rgba(255, 240, 200, 0.7);
    padding: 0;
    margin: 0;
    color: #5c4728;
    font-size: 18px;
    width: 100%;
}

/* Style de l'espace réservé (placeholder) */
div[class^="stTextInput"] input::placeholder {
    color: #5c4728aa;
}

/* Cache le label inutile */
div[data-testid="stTextInput"] label {
    display: none;
}

/* Icône de loupe intégrée */
div[class^="stTextInput"] > div::after {
    content: "🔍";
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 18px;
    color: white;
    background-color: #FDF5E6;
    border-radius: 8px;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: 2px solid white;
    pointer-events: none;                               /* permet de cliquer dans le champ input */
}
</style>
"""

# --- 2. INJECTION DU CSS (Ligne manquante) ---
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. WIDGET DE SAISIE DE TEXTE ---
recherche_film = st.text_input(
    label="", # Label vide, géré par le CSS
    placeholder="Rentrez le nom d'un film...",
    key="search_input"
)

# Affichage du résultat pour vérifier
if recherche_film:
    st.info(f"Recherche lancée pour : **{recherche_film}**")


