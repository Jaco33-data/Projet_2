import streamlit as st
import pandas as pd
import base64





# ----------------------------------------------------------------------
# --- Dataframe
df_film = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_movie.csv")
df_ml = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_ML.csv")
df_intervenant = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_intervenant.csv")

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
df_film_5 = df_film.head(5)

recherche_film = st.text_input(label="",placeholder="Que la magie du ML opére !", label_visibility="collapsed")
reco = recherche_film

# ----------------------------------------------------------------------
# --- IMAGES FILMS (GAUCHE)

# --- Affiche films
def affiche(indice):
        film_reco = df_film_5.iloc[indice]
#        film = df_film_5[df_film_5['tconst'] == film_reco]
        image = film_reco[12]
        return image

# --- Vidéo films
def trailer(indice):
        film_reco = df_film_5.iloc[indice]
        video = film_reco[-1]
        return video

# --- Affichage des 5 affiches
if "film_selected" not in st.session_state:
    st.session_state.film_selected = None

# --- Container HTML gauche
films_html = '<div class="films-container">'
for i in range(5):
    url = affiche(i)
    films_html += f'<img src="{url}">'
films_html += '</div>'

st.markdown(films_html, unsafe_allow_html=True)






# --- Affichage de la bande annonce
if st.session_state.film_selected is not None:
    video_url = trailer(st.session_state.film_selected)
    st.markdown(
        f"""
        <div class="video-container">
            <div class="custom-video">
                <iframe src="{video_url}" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

#films_html = '<div class="films-container">'
#for i in range(5):
#       url = affiche(i)
#       films_html += f'<img src="{url}">'
#films_html += '</div>'
#st.markdown(films_html, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- IMAGES ACTEURS (DROITE)

def affiche_intervenants(indice):
       film_reco = reco[indice]
       intervenant = df_intervenant[df_intervenant['movie_id'] == film_reco]
       poster_1 = intervenant.iloc[0,3]
       poster_2 = intervenant.iloc[1,3]
       poster_3 = intervenant.iloc[2,3]
       return [poster_1,poster_2, poster_3]

    

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
# --- VIGNETTE "ACTORS"
st.markdown("""
<div class="intervenant-badge">
    Intervenants
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# --- VIDEO + SYNOPSIS (dans container HTML pour position libre)
#    width="1000" height="800"
#def trailer(indice):
#        film_reco = reco[indice]
#        film = df_film[df_film['tconst'] == film_reco]
#        video = film.iloc[-1]
#        if video.isnull() == True:
#               video = "C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\Video_trailer_manquant.mp4"
#        return video


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