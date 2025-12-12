import streamlit as st
import pandas as pd
import base64
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ----------------------------------------------------------------------
# --- Machine Learning
# Création d'une variable avec un input pour que l'utilisateur puisse choisirs le film qu'il a vu
df_film = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_movie.csv")
research_film = input("Rentrez le nom d'un film : ")
votre_film = df_film[df_film['tconst']== id] # Variable qui stocke le film sur le qule se base la reco
# changer le chemin d'accès
def ml_recommandation(research_film) :
  df_ml = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_ML.csv")
  research_film = research_film.lower().capitalize()
  df_film_user = df_ml[df_ml['title_x'].str.contains(research_film)]
  id = df_film_user.iloc[0, 1]
  # Sélection des colonnes à garder pour le film entré par l'utilisateur
  movie_user = df_film_user.drop(columns=['tconst', 'title_x'])
  df_reco = df_ml[df_ml['title_x'].str.contains(research_film)== False]
  X = df_reco.drop(columns=['title_x', 'tconst'])
  model = NearestNeighbors(n_neighbors=5) # Définition du modèle
  model.fit(X) # Entrainement sur les features utilisé pour la recommandation
  # répertorie la distance et les indices des 5 films recommandé par rapport au film vu par l'utilisateur
  distance, indices = model.kneighbors(movie_user)
  reco_indices = indices[0,] # Sélectionne toute la ligne des films recommandés

  recommandations = df_ml.iloc[reco_indices,1] # variables qui stockes les films recommandés

  return recommandations
recommandation = ml_recommandation

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
def affiche(indice):
        film_reco = reco[indice]
        film = df_film[df_film['tconst'] == film_reco]
        image = film.iloc[0, 12]
        return image
films = """
<div class="left-container">
    <img src= affiche(0) class="col1-top-left">
    <img src= affiche(1) class="col2-top-middle">
    <img src= affiche(2) class="col3-top-right">
    <img src= affiche(3) class="col4-bottom-left">
    <img src= affiche(4) class="col5-bottom-middle">
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
# --- VIDEO + SYNOPSIS (dans container HTML pour position libre)
st.markdown("""
<div class="video-container">
    <div class="custom-video">
        <iframe width="1000" height="800" src="https://www.youtube.com/embed/M7lcd68a9HQ" frameborder="0" allowfullscreen></iframe>
    </div>
    <div class="synopsis-box">
        Voici le résumé du film !
    </div>
</div>
""", unsafe_allow_html=True)

# --- BOUTON (optionnel pour interactivité)
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
recherche = st.text_input(research_film, label_visibility="collapsed")
reco = ml_recommandation(recherche)

