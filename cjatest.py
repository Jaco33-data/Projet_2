import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import base64

# --- CONFIGURATION PAGE ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df_film = pd.read_csv(r"C:\Users\carin\Desktop\Formation Data Analyst\99. Projets\P2 - Recommandations de films\Streamlit\df_FINAL_movie.csv")
    df_ml = pd.read_csv(r"C:\Users\carin\Desktop\Formation Data Analyst\99. Projets\P2 - Recommandations de films\Streamlit\df_ML.csv")
    df_inter = pd.read_csv(r"C:\Users\carin\Desktop\Formation Data Analyst\99. Projets\P2 - Recommandations de films\Streamlit\df_FINAL_intervenant.csv")
    return df_film, df_ml, df_inter

df_film, df_ml, df_inter = load_data()

# --- CSS & FOND ---
def apply_style():
    path_fond = r"C:\Users\carin\Desktop\Formation Data Analyst\99. Projets\P2 - Recommandations de films\Streamlit\images\Gemini_Generated_Image_fond.png"
    with open(path_fond, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    /* Fond d'écran */
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
    }}
    header, footer {{visibility: hidden;}}
    .block-container {{padding: 0px;}}

    .cinema-title {{
        text-align: center;
        color: white;
        font-family: 'Great Vibes', cursive;
        font-size: 45px;
        margin-top: 10px;
        text-shadow: 2px 2px 4px #000;
    }}

    .badge-box {{
        background: rgba(0, 0, 0, 0.6);
        color: white;
        font-family: 'Great Vibes', cursive;
        font-size: 24px;
        text-align: center;
        border: 1px solid gold;
        border-radius: 10px;
        padding: 5px;
        margin-bottom: 15px;
    }}

    .video-screen {{
        border: 10px solid #1a1a1a;
        background: black;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }}

    .synopsis-area {{
        background: rgba(0, 0, 0, 0.8);
        color: #fff;
        padding: 10px;
        border: 1px solid #444;
        border-radius: 5px;
        font-size: 14px;
        margin-top: 5px;
    }}

    div.stButton > button {{
        width: 100%;
        background-color: rgba(255, 215, 0, 0.1);
        color: gold;
        border: 1px solid gold;
        font-size: 12px;
        margin-top: 5px;
        margin-bottom: 15px;
        border-radius: 5px;
        cursor: pointer;
    }}

    </style>
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

apply_style()

# --- SESSION STATE ---
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'reco_list' not in st.session_state:
    st.session_state.reco_list = []

# --- MACHINE LEARNING ---
def get_recommendations(movie_title):
    try:
        query_film = df_ml[df_ml['title_x'].str.contains(movie_title, case=False, na=False)].iloc[0:1]
        X = df_ml.drop(columns=['title_x', 'tconst']).fillna(0)
        model = NearestNeighbors(n_neighbors=6, metric='cosine').fit(X)
        _, indices = model.kneighbors(query_film.drop(columns=['title_x', 'tconst']).fillna(0))
        return df_ml.iloc[indices[0][1:]]['tconst'].tolist()
    except:
        return []

# --- INTERFACE ---
st.markdown('<div class="cinema-title">Le site de recommandations ciblé et pertinent</div>', unsafe_allow_html=True)

# Barre de recherche
_, col_search, _ = st.columns([1, 2, 1])
with col_search:
    search_input = st.selectbox(
        "", options=df_film["title_x"].unique(), index=None,
        placeholder="Que la magie du ML opère !", label_visibility="collapsed"
    )

# Mettre à jour recommandations et film sélectionné
if search_input:
    recos = get_recommendations(search_input)
    if recos:
        st.session_state.reco_list = recos
        if st.session_state.selected_movie is None or st.session_state.selected_movie not in recos:
            st.session_state.selected_movie = recos[0]

# --- LAYOUT PRINCIPAL ---
col_L, col_C, col_R = st.columns([1, 2, 1])

# --- COLONNE GAUCHE : AFFICHES + BOUTONS ---
with col_L:
    st.markdown('<div style="margin-top:80px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-box">Films</div>', unsafe_allow_html=True)
    for i, tid in enumerate(st.session_state.reco_list):
        film_info = df_film[df_film['tconst'] == tid].iloc[0]
        st.image(film_info.iloc[12], width=130)
        # Bouton unique avec clé combinée
        if st.button("SÉLECTIONNER", key=f"{tid}_{i}"):
            st.session_state.selected_movie = tid
            st.rerun()

# --- COLONNE CENTRALE : VIDEO + SYNOPSIS ---
with col_C:
    st.markdown('<div style="margin-top:50px;"></div>', unsafe_allow_html=True)
    if st.session_state.selected_movie:
        movie_data = df_film[df_film['tconst'] == st.session_state.selected_movie].iloc[0]
        url_vid = movie_data.iloc[-1]
        st.markdown('<div class="video-screen">', unsafe_allow_html=True)
        if isinstance(url_vid, str) and "http" in url_vid:
            st.video(url_vid)
        else:
            st.info("Bande-annonce non disponible")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="synopsis-area"><b>Voici le résumé du film :</b><br>{movie_data.iloc[11]}</div>', unsafe_allow_html=True)

# --- COLONNE DROITE : INTERVENANTS ---
with col_R:
    st.markdown('<div style="margin-top:80px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-box">Intervenants</div>', unsafe_allow_html=True)
    if st.session_state.selected_movie:
        acteurs = df_inter[df_inter['tconst'] == st.session_state.selected_movie].head(3)
        if not acteurs.empty:
            for _, actor in acteurs.iterrows():
                st.image(actor.iloc[3], caption=actor.iloc[1], width=110)
        else:
            st.write("Infos acteurs non disponibles")