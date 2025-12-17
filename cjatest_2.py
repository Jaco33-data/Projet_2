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

# --- CSS & FOND RECADRÉ ---
def apply_style():
    path_fond = r"C:\Users\carin\Desktop\Formation Data Analyst\99. Projets\P2 - Recommandations de films\Streamlit\images\Gemini_Generated_Image_fond.png"
    try:
        with open(path_fond, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
    except: encoded = ""

    st.markdown(f"""
    <style>
    /* Fond d'écran avec cadrage précis */
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center center; /* Cadrage central comme sur l'image */
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    header, footer {{visibility: hidden;}}
    .block-container {{padding: 0px;}}

    .cinema-title {{
        text-align: center;
        color: white;
        font-family: 'Great Vibes', cursive;
        font-size: 55px; /* Augmenté pour la visibilité */
        margin-top: 20px;
        text-shadow: 3px 3px 6px #000;
    }}

    .badge-box {{
        background: rgba(0, 0, 0, 0.8);
        color: gold;
        font-family: 'Great Vibes', cursive;
        font-size: 28px;
        text-align: center;
        border: 2px solid gold;
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 20px;
    }}

    .video-screen {{
        border: 12px solid #1a1a1a;
        background: black;
        box-shadow: 0px 0px 30px rgba(0,0,0,0.7);
        margin-bottom: 15px;
    }}

    .synopsis-area {{
        background: rgba(0, 0, 0, 0.9);
        color: #fff;
        padding: 15px;
        border: 1px solid gold;
        border-radius: 8px;
        font-size: 16px;
        line-height: 1.4;
        text-align: justify;
    }}

    div.stButton > button {{
        width: 100%;
        background-color: gold !important;
        color: black !important;
        font-weight: bold !important;
        border: 1px solid black;
        border-radius: 5px;
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

# --- MACHINE LEARNING (ZÉRO DOUBLON) ---
def get_recommendations(movie_title):
    try:
        query_film = df_ml[df_ml['title_x'].str.contains(movie_title, case=False, na=False)].iloc[0:1]
        tconst_original = query_film['tconst'].values[0]
        
        X = df_ml.drop(columns=['title_x', 'tconst']).fillna(0)
        model = NearestNeighbors(n_neighbors=15, metric='cosine').fit(X) # On en cherche plus pour filtrer
        _, indices = model.kneighbors(query_film.drop(columns=['title_x', 'tconst']).fillna(0))
        
        # Récupération des tconst uniques et différents du film cherché
        potential_recos = df_ml.iloc[indices[0]]['tconst'].unique().tolist()
        final_recos = [t for t in potential_recos if t != tconst_original][:5]
        
        return final_recos
    except:
        return []

# --- INTERFACE ---
st.markdown('<div class="cinema-title">Le site de recommandations ciblé et pertinent</div>', unsafe_allow_html=True)

_, col_search, _ = st.columns([1, 2, 1])
with col_search:
    search_input = st.selectbox(
        "", options=df_film["title_x"].unique(), index=None,
        placeholder="Entrez un film pour lancer la magie...", label_visibility="collapsed"
    )

if search_input:
    recos = get_recommendations(search_input)
    if recos:
        st.session_state.reco_list = recos
        # Initialise avec le premier film si rien n'est sélectionné
        if st.session_state.selected_movie not in recos:
            st.session_state.selected_movie = recos[0]

# --- AFFICHAGE ---
if st.session_state.reco_list:
    col_L, col_C, col_R = st.columns([1, 2.2, 1])

    with col_L:
        st.markdown('<div style="margin-top:60px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="badge-box">Films</div>', unsafe_allow_html=True)
        for i, tid in enumerate(st.session_state.reco_list):
            film_info = df_film[df_film['tconst'] == tid].iloc[0]
            st.image(film_info.iloc[12], width=140)
            if st.button("VOIR", key=f"btn_{tid}_{i}"):
                st.session_state.selected_movie = tid
                st.rerun()

    with col_C:
        st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
        if st.session_state.selected_movie:
            movie_data = df_film[df_film['tconst'] == st.session_state.selected_movie].iloc[0]
            url_vid = movie_data.iloc[-1]
            st.markdown('<div class="video-screen">', unsafe_allow_html=True)
            if isinstance(url_vid, str) and "http" in url_vid:
                st.video(url_vid)
            else:
                st.info("Bande-annonce non disponible")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="synopsis-area"><b>RÉSUMÉ :</b><br>{movie_data.iloc[11]}</div>', unsafe_allow_html=True)

    with col_R:
        st.markdown('<div style="margin-top:60px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="badge-box">Intervenants</div>', unsafe_allow_html=True)
        if st.session_state.selected_movie:
            acteurs = df_inter[df_inter['tconst'] == st.session_state.selected_movie].head(3)
            for _, actor in acteurs.iterrows():
                st.image(actor.iloc[3], width=120)
                st.write(f"**{actor.iloc[1]}**")