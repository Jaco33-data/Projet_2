import streamlit as st
import pandas as pd
import base64
from st_clickable_images import clickable_images
from sklearn.neighbors import NearestNeighbors


# 1. CONFIGURATION DE LA PAGE
st.set_page_config(layout="wide")


# 2. ÉTAT DE LA SESSION (Initialisation)
if "page" not in st.session_state:
    st.session_state.page = 1
if "film_selected" not in st.session_state:
    st.session_state.film_selected = None


# ================= PAGE 1 : INTRO VIDÉO =================
if st.session_state.page == 1:
    try:
        with open("video_ouverture.mp4", "rb") as f:
            video_base64 = base64.b64encode(f.read()).decode()


        st.markdown(f"""
            <style>
            .block-container {{ padding: 0 !important; margin: 0 !important; max-width: 100% !important; }}
            header, footer {{ display: none !important; }}
            .video-bg {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; overflow: hidden; }}
            .video-bg video {{ width: 100vw; height: 100vh; object-fit: cover; }}
            div.stButton {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999; display: flex; align-items: center; justify-content: center; }}
            div.stButton > button {{ width: 100vw !important; height: 100vh !important; background-color: transparent !important; color: transparent !important; border: none !important; cursor: pointer !important; }}
            </style>
            <div class="video-bg">
                <video autoplay loop muted playsinline>
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """, unsafe_allow_html=True)


        if st.button("ENTRER", key="skip_btn"):
            st.session_state.page = 2
            st.rerun()
        st.stop()
    except FileNotFoundError:
        st.session_state.page = 2 # Si la vidéo manque, on passe à la page 2


# ================= PAGE 2 : RECOMMANDATIONS =================


# --- Chargement des données ---
@st.cache_data
def load_data():
    df_f = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_FINAL_movie.csv")
    df_m = pd.read_csv("C:\\Users\\carin\\Desktop\\Formation Data Analyst\\99. Projets\\P2 - Recommandations de films\\Streamlit\\df_ML.csv")
    return df_f, df_m


df_film, df_ml = load_data()


# --- Fonctions ML ---
def ml_recommandation(research_film):
    film_to_find = research_film.strip().lower()
    df_film_user = df_ml[df_ml['title_x'].str.contains(film_to_find, case=False, na=False)]
    if df_film_user.empty: return pd.Series(dtype='object')
    
    df_film_user = df_film_user.iloc[0:1]
    df_reco = df_ml[df_ml.index != df_film_user.index[0]].drop_duplicates()
    X = df_reco.drop(columns=['title_x', 'tconst'], errors='ignore').fillna(0)
    features_cols = X.columns
    movie_user = df_film_user[features_cols].fillna(0)
    
    model = NearestNeighbors(n_neighbors=5, metric='cosine')
    model.fit(X)
    _, indices = model.kneighbors(movie_user)
    return df_reco.iloc[indices[0]]['tconst']


def affiche(indice, reco_series):
    tconst_id = reco_series.iloc[indice]
    film = df_film[df_film['tconst'] == tconst_id]
    return film.iloc[0, 12] if not film.empty else ""


# --- CSS GLOBAL & FOND ---
#with open("assets/style.css", encoding='utf-8') as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#with open("images/Gemini_Generated_Image_fond.png", "rb") as f:
#    encoded_bg = base64.b64encode(f.read()).decode()


#st.markdown(f"""
#    <style>
#    body {{ background-image: url("data:image/png;base64,{encoded_bg}"); background-attachment: fixed; background-size: cover; }}
#    .stApp {{ background: transparent !important; }}
#    </style>
#    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
#    """, unsafe_allow_html=True)


# --- BARRE DE RECHERCHE ---
recherche_film = st.selectbox(
    label="", options=df_film["title_x"].tolist(), index=None,
    placeholder="Que la magie du ML opère !", label_visibility="collapsed"
)


# --- AFFICHAGE DES IMAGES CLIQUABLES (GAUCHE) ---
if recherche_film:
    reco = ml_recommandation(recherche_film)
    if not reco.empty:
        images_urls = [affiche(i, reco) for i in range(len(reco))]
        
        # Utilisation du composant clickable_images avec votre style exact
        clicked_index = clickable_images(
            images_urls,
            titles=[f"Film {i}" for i in range(len(reco))],
            div_style={
                "display": "flex", "justify-content": "flex-start", "flex-wrap": "wrap", 
                "gap": "30px", "position": "absolute", "top": "550px", "left": "5%", 
                "width": "750px", "z-index": "5000"
            },
            img_style={"cursor": "pointer", "border-radius": "18px", "width": "200px", "transition": "0.3s"},
            key="movie_gallery"
        )
        
        if clicked_index > -1:
            st.session_state.film_selected = reco.iloc[clicked_index]
            st.rerun()
else:
    st.markdown('<div class="film-badge" style="top:550px; left:5%;">Saisissez un film !</div>', unsafe_allow_html=True)


# --- TRAILER & SYNOPSIS ---
url_video = None
texte_synopsis = "Voici le résumé du film !"


if st.session_state.film_selected:
    m_id = st.session_state.film_selected
    film_data = df_film[df_film['tconst'] == m_id]
    if not film_data.empty:
        # URL Vidéo
        raw_v = film_data.iloc[0, -1]
        if isinstance(raw_v, str) and "http" in raw_v:
            if "youtube.com" in raw_v:
                url_video = raw_v.replace("watch?v=", "embed/") + "?autoplay=0"
            elif "youtu.be" in raw_v:
                url_video = f"https://www.youtube.com/embed/{raw_v.split('/')[-1]}?autoplay=0"
        
        # Synopsis
        raw_s = film_data.iloc[0, 11]
        texte_synopsis = raw_s if isinstance(raw_s, str) else "Synopsis indisponible."


if url_video:
    st.markdown(f"""
    <div class="video-container">
        <div class="custom-video">
            <iframe src="{url_video}" frameborder="0" allowfullscreen style="width:1200px; height:580px;"></iframe>
        </div>
        <div class="synopsis-box">{texte_synopsis}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f'<div class="video-container"><div class="synopsis-box">Cliquez sur une affiche pour voir le trailer.</div></div>', unsafe_allow_html=True)


# --- ÉLÉMENTS DÉCORATIFS (TITRE ET BADGES) ---
st.markdown('<h1 class="title">Le site de recommandations ciblé et pertinent</h1>', unsafe_allow_html=True)
st.markdown('<div class="film-badge">Films</div>', unsafe_allow_html=True)
st.markdown('<div class="intervenant-badge">Intervenants</div>', unsafe_allow_html=True)


# --- ACTEURS (DROITE) ---
intervenants_html = """
<div class="right-container">
    <img src="https://static.streamlit.io/examples/cat.jpg" class="image1-top-left">
    <img src="https://static.streamlit.io/examples/dog.jpg" class="image2-top-middle">
    <img src="https://static.streamlit.io/examples/owl.jpg" class="image3-top-right">
</div>
"""
st.markdown(intervenants_html, unsafe_allow_html=True)
