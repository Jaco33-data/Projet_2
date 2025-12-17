import streamlit as st
import pandas as pd
import base64

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# ----------------------------------------------------------------------
# --- Machine Learning
# Création d'une variable avec un input pour que l'utilisateur puisse choisirs le film qu'il a vu
df_film = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_movie.csv")


def ml_recommandation(research_film) :
  df_ml = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_ML.csv")
  film_to_find = research_film.strip().lower()
  df_film_user = df_ml[df_ml['title_x'].str.contains(film_to_find, case=False, na=False)]
  if df_film_user.empty:
        print(f"Erreur : Aucun film correspondant à '{research_film}' n'a été trouvé dans le DataFrame.")
        return pd.Series(dtype='object')
  df_film_user = df_film_user.iloc[0:1]
  df_reco = df_ml[df_ml.index != df_film_user.index[0]].drop_duplicates()
  cols_to_drop = ['title_x', 'tconst']
  X = df_reco.drop(columns=cols_to_drop, errors='ignore') # Jeu d'entraînement
  features_cols = X.columns 
  movie_user = df_film_user[features_cols]
  movie_user = movie_user.fillna(0)
  if movie_user.isnull().values.any() or movie_user.empty:
        print(f"Erreur : Le film '{research_film}' a des données invalides pour la modélisation.")
        return pd.Series(dtype='object')
  try:
        model = NearestNeighbors(n_neighbors=5, metric='cosine') 
        model.fit(X)
        distance, indices = model.kneighbors(movie_user) 
        reco_indices = indices[0,]
        recommandations = df_reco.iloc[reco_indices]['tconst']
        return recommandations
  except Exception as e:
        print(f"Erreur de modélisation : {e}")
        return pd.Series(dtype='object')

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
# --- BARRE DE RECHERCHE
#recherche_film = st.text_input(label="",placeholder="Que la magie du ML opére !", label_visibility="collapsed")
recherche_film = st.selectbox(
    label="",
    options=df_film["title_x"].tolist(),
    index=None,
    placeholder="Que la magie du ML opère !",
    label_visibility="collapsed"
)

# ----------------------------------------------------------------------
# --- IMAGES FILMS (GAUCHE)
def affiche(indice):
        film_reco = reco.iloc[indice]
        film = df_film[df_film['tconst'] == film_reco]
        if film.empty:
            return "URL_IMAGE_DEFAUT"
        film_tconst = film.iloc[0]['tconst']
        image = film.iloc[0,12]
        return image

# --- Affichage des 5 affiches
if "film_selected" not in st.session_state:
    st.session_state.film_selected = None

# --- Container HTML gauche
films_html = '<div class="films-container">'
if recherche_film:
    reco = ml_recommandation(recherche_film)  
    for i in range(5):
        url = affiche(i)
        films_html += f'<img src="{url}">'
else:
    films_html += '<p>Aucune recommandation disponible, saisissez un film ci-dessus !</p>'

films_html += '</div>'

st.markdown(films_html, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# --- IMAGES ACTEURS (DROITE)
#df_intervenant = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_intervenant.csv")

#def affiche_intervenants(indice):
#       film_reco = reco[indice]
#       intervenant = df_intervenant[df_intervenant['movie_id'] == film_reco]
#       poster_1 = intervenant.iloc[0,3]
#       poster_2 = intervenant.iloc[1,3]
#       poster_3 = intervenant.iloc[2,3]
#       return [poster_1,poster_2, poster_3]


intervenants = """
<div class="right-container">
    <img src="https://static.streamlit.io/examples/cat.jpg" class="image1-top-left">
    <img src="https://static.streamlit.io/examples/dog.jpg" class="image2-top-middle">
    <img src="https://static.streamlit.io/examples/owl.jpg" class="image3-top-right">
</div>
"""
st.markdown(intervenants, unsafe_allow_html=True)

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
# --- VIGNETTE "INTERVENANTS"
st.markdown("""
<div class="intervenant-badge">
    Intervenants
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- VIDEO + SYNOPSIS (dans container HTML pour position libre)
#    width="1000" height="800"
def trailer(indice):
        film_reco = reco[indice]
        film = df_film[df_film['tconst'] == film_reco]
        video = film.iloc[-1]
        if video.isnull() == True:
               video = "C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\Video_trailer_manquant.mp4"
        return video

def synopsis(indice):
        film_reco = reco[indice]
        film = df_film[df_film['tconst'] == film_reco]
        syno = film.iloc[0, 11]
        if syno.isnull() == True:
               syno = "En attendant le synopsis officiel, laissez-nous vous conter l’histoire de Creusette :" \
               "Creusette est une vache pas comme les autres : plutôt que de se contenter de brouter dans son pré, elle rêve de projecteurs, de pop-corn et de grands écrans. " \
               "Un jour, prenant son courage a deux sabots elle décide de suivre ses ambitions. Elle s’échappe de son enclos et traverse le pays, pour réaliser son rêve fou. " \
               "Dans le creux d'une vallée isolée, elle bâtit le tout premier cinéma de Creuse… devenu le rendez-vous incontournable des humains… et des animaux critiques de films. " \
               "Entre humour, aventures inattendues et lait frais servi à volonté, Creusette prouve qu’aucun rêve n’est trop grand, même pour une vache."
        return syno

st.markdown("""
<div class="video-container">
    <div class="custom-video">
        <iframe src="https://www.youtube.com/embed/M7lcd68a9HQ" frameborder="0" allowfullscreen></iframe>
    </div>
    <div class="synopsis-box">
        Voici le résumé du film !
    </div>
</div>
""", unsafe_allow_html=True)





