import streamlit as st
import pandas as pd
import base64# Injection du lien de la police 'Great Vibes' via <link>
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

st.markdown(f"""<style>
    body {{background-image: url("data:image/png;base64,{encoded}");
    }}
    </style>
    """, unsafe_allow_html=True)

# -- Création des blocs FILMS & ACTEURS
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

# -- Ordre vertical dans le streamlit
# Titre
st.markdown(f"""<h1 class="title">Le site de recommandations ciblé et pertinent</h1>
    """, unsafe_allow_html=True)


# Ecran Bande Annonce
with st.container():
    # Utilisé pour forcer le centrage de la vidéo et du bouton au centre de la page
    col_gauche, col_centre, col_droite = st.columns([1, 4, 1])
    
    with col_centre:
        # La vidéo n'est plus en fixed, elle suit le flux normal de la colonne
        st.video("https://www.youtube.com/watch?v=M7lcd68a9HQ")

# Bouton Synopsis (le CSS positionne ce bouton au bon endroit)
with st.container():
    col_gauche_btn, col_btn, col_droite_btn = st.columns([2, 1, 2])
    with col_btn:
        if st.button("Synopsis"):
            st.markdown(
                """<div style='text-align: center; font-size: 20px;'>
                   Voici le résumé du film !
                   </div>""", 
                unsafe_allow_html=True)

# Barre de recherche
st.text_input("Rentrez le nom d'un film...", label_visibility="collapsed")



# --- 3. WIDGET DE SAISIE DE TEXTE ---
#recherche_film = st.text_input(
    #label="", # Label vide, géré par le CSS
    #placeholder="Rentrez le nom d'un film...",
    #key="search_input"
#)
# Affichage du résultat pour vérifier
#if recherche_film:
    #st.info(f"Recherche lancée pour : **{recherche_film}**")


