import streamlit as st
import pandas as pd
import base64

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from st_clickable_images import clickable_images


st.set_page_config(layout="wide")

# ---------------- ÉTAT ----------------
if "page" not in st.session_state:
    st.session_state.page = 1


# ================= PAGE 1 : INTRO VIDÉO =================
if st.session_state.page == 1:


    with open("video_ouverture.mp4", "rb") as f:
        video_base64 = base64.b64encode(f.read()).decode()


    # --- CSS SPÉCIAL PAGE 1 ---
    st.markdown(
        f"""
        <style>
        /* Nettoyage de l'interface de base */
        .block-container {{ padding: 0 !important; margin: 0 !important; max-width: 100% !important; }}
        header, footer {{ display: none !important; }}
       
        /* 1. LA VIDÉO (Au fond) */
        .video-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            overflow: hidden;
        }}
        .video-bg video {{
            width: 100vw;
            height: 100vh;
            object-fit: cover;
        }}


        /* 2. LE BOUTON (Au dessus) */
        /* On cible le conteneur du bouton Streamlit */
        div.stButton {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 999999; /* Toujours au-dessus */
            display: flex;
            align-items: center;
            justify-content: center;
        }}


        /* On cible le bouton lui-même */
        div.stButton > button {{
            width: 100vw !important;
            height: 100vh !important;
            background-color: transparent !important; /* Fond invisible */
            color: transparent !important; /* Texte invisible */
            border: none !important;
            outline: none !important;
            cursor: pointer !important; /* Force le curseur 'main' */
        }}
       
        /* Au survol, on garde tout invisible */
        div.stButton > button:hover, div.stButton > button:active, div.stButton > button:focus {{
            background-color: transparent !important;
            color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        </style>


        <div class="video-bg">
            <video autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --- LE BOUTON INVISIBLE ---
    # On met du texte pour garantir que la zone de clic existe, mais le CSS le cache.
    if st.button("CLIQUE_ICI_POUR_ENTRER", key="skip_btn"):
        st.session_state.page = 2
        st.rerun()

    st.stop()

# ----------------------------------------------------------------------
# --- Machine Learning
# Création d'une variable avec un input pour que l'utilisateur puisse choisirs le film qu'il a vu
df_film = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_movie.csv")
df_ml = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_ML.csv")

def ml_recommandation(research_film) :
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

# --- Style bouton
st.markdown("""
<style>
img {
    border-radius: 18px;
}
button {
    border-radius: 12px;
    transition: 0.3s ease;
}
button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# --- Container HTML gauche
#films_html = '<div class="films-container">'
# Remplacement de l'affichage par st_clickable_images
if recherche_film:
    reco = ml_recommandation(recherche_film)
    if not reco.empty:
        # On limite à 5 recommandations ou moins si pas assez de résultats
        num_recos = min(5, len(reco))
        
        images_urls = []
        titles_list = []
        tconst_list = []
        
        for i in range(num_recos):
            images_urls.append(affiche(i))
            titles_list.append(f"Film {i+1}") # Titres pour l'accessibilité si nécessaire
            tconst_list.append(reco.iloc[i])
            
        # Affichage interactif des images cliquables
        clicked_index = clickable_images(
            images_urls,
            titles=titles_list,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "gap": "20px"},
            img_style={"cursor": "pointer", "border-radius": "18px", "transition": "transform 0.3s", "height": "300px"},
            key="gallery" # Clé unique pour le composant
        )
        
        # Gestion du clic : si une image est cliquée, on met à jour la session_state
        if clicked_index > -1:
             selected_tconst = tconst_list[clicked_index]
             # Mise à jour seulement si nouveau film sélectionné pour éviter boucle infinie
             if st.session_state.film_selected != selected_tconst:
                 st.session_state.film_selected = selected_tconst
                 st.rerun()

# --- Placeholder pour l'ancien code HTML (supprimé)
films_html = ""

#--- Récupération des données du film sélectionné
url_video = "Video_trailer_manquant.mp4" # Par défaut
texte_synopsis = "Voici le résumé du film !"

if st.session_state.film_selected:
    m_id = st.session_state.film_selected

    film_data = df_film[df_film['tconst'] == m_id]

    if not film_data.empty:
        # URL Vidéo (supposée être en dernière colonne)
        raw_v = film_data.iloc[0, -1]
        
        if isinstance(raw_v, str) and "http" in raw_v:
            if "youtube.com" in raw_v:
                url_video = raw_v.replace("watch?v=", "embed/")
            elif "youtu.be" in raw_v:
                 # Transformation youtu.be/ID -> youtube.com/embed/ID
                 video_id = raw_v.split("/")[-1]
                 url_video = f"https://www.youtube.com/embed/{video_id}"
            else:
                url_video = raw_v # Autres formats, on espère que c'est embeddable

        # Synopsis (colonne 11)
        raw_s = film_data.iloc[0, 11]
        if isinstance(raw_s, str):
            texte_synopsis = raw_s

# Affichage de l'iframe ou message d'erreur
html_content = ""
if url_video:
    html_content = f"""
    <div class="video-container">
        <div class="custom-video">
            <iframe src="{url_video}" frameborder="0" allowfullscreen style="width:100%; height:100%;"></iframe>
        </div>
        <div class="synopsis-box">
            {texte_synopsis}
        </div>
    </div>
    """
else:
    html_content = f"""
    <div class="video-container">
        <div class="synopsis-box" style="text-align: center; padding: 50px;">
            <h3>🚫 Trailer indisponible</h3>
            <p>Nous n'avons pas trouvé de bande-annonce pour ce film.</p>
        </div>
        <div class="synopsis-box">
            {texte_synopsis}
        </div>
    </div>
    """

st.markdown(html_content, unsafe_allow_html=True)

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


