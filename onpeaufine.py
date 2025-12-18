import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import base64

# --- CONFIGURATION PAGE ---
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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
        font-family: 'Great Vibes', cursive !important;
        font-size: 70px;
        margin-top: 10px;
        text-shadow: 3px 3px 6px #000;
        margin-bottom: 30px;
        z-index: 1000;
        position: relative;
    }}

    div[class^="stSelectbox"] {{
        position: fixed;
        top: 200px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 3000;
        width: 700px; 
        height: 90px;
    }}

    div[data-testid="stSelectbox"] > div:nth-child(2) > div {{
        background-color: #FDF5E6 !important;
        border-radius: 40px;
        border: 5px solid #D0A372; / Bordure un peu plus fine pour l'équilibre /
        min-height: 65px !important;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4)
}}

    div[data-testid="stSelectbox"] input, div[data-testid="stSelectbox"] div[role="button"] {{
        font-size: 20px !important;
        color: black !important;
    }}

    div[data-testid="stSelectbox"] > div:nth-child(2) > div:focus-within {{
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }}

    .badge-box {{
        background: rgba(0, 0, 0, 0.5);
        color: white;
        font-family: 'Great Vibes', cursive !important;
        font-size: 50px;
        text-align: center;
        border: 4px solid white;
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
        background: rgba(0, 0, 0, 0.5);
        color: #fff;
        padding: 15px;
        border: 1px solid white;
        border-radius: 8px;
        font-size: 20px;
        line-height: 1.4;
        text-align: justify;
    }}

    div.stButton > button {{
        width: 100%;
        background-color: rgba (255, 215, 0, 0.8) !important;
        color: black !important;
        font_size:10 px !important;
        padding: 2PX !important;
        height: 25PX !important;
        border-radius: 4px;
        border: none;
    }}

    [data-testid="stImage"] img {{
        border-radius: 8px;
        border: 1px solid gold;
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
st.markdown('<div class="cinema-title">On ne sait jamais, sur un malendu ça peut marcher</div>', unsafe_allow_html=True)

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
        c1, c2, c3 = st.columns(3)
        for i in range(min(3, len(st.session_state.reco_list))):
            tid = st.session_state.reco_list[i]
            film_info = df_film[df_film['tconst'] == tid].iloc[0]
            with [c1, c2, c3][i]:
                st.image(film_info.iloc[12], use_container_width=True)
                if st.button("VOIR", key=f"btn_{tid}_{i}"):
                    st.session_state.selected_movie = tid
                    st.rerun()
        if len(st.session_state.reco_list) > 3:
            st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
            # On utilise 4 colonnes pour centrer les 2 films au milieu
            _, c4, c5, _ = st.columns([0.5, 1, 1, 0.5])
            for i in range(3, min(5, len(st.session_state.reco_list))):
                tid = st.session_state.reco_list[i]
                film_info = df_film[df_film['tconst'] == tid].iloc[0]
                with [c4, c5][i-3]:
                    st.image(film_info.iloc[12], use_container_width=True)
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
                st.video("Video_trailer_manquant.mp4")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="synopsis-area"><b>RÉSUMÉ :</b><br>{movie_data.iloc[11]}</div>', unsafe_allow_html=True)

    with col_R:
        st.markdown('<div style="margin-top:60px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="badge-box">Intervenants</div>', unsafe_allow_html=True)
        if st.session_state.selected_movie:
            # Filtrer et trier les intervenants par popularité
            top_intervenants = df_inter[df_inter['movie_id'] == st.session_state.selected_movie] \
                                .sort_values(by='popularity', ascending=False) \
                                .head(3)
            
            if not top_intervenants.empty:
                for _, actor in top_intervenants.iterrows():
                    # --- SÉCURITÉ IMAGE ---
                    img_url = actor.loc['full_image_url'] # L'URL de l'image
                    nom_acteur = actor.iloc[0] # Le nom
                    

                    if not isinstance(img_url, str) or pd.isna(img_url) or img_url.lower() == "nan":
                        img_url = r"C:\Users\carin\Desktop\Formation Data Analyst\99. Projets\P2 - Recommandations de films\Streamlit\images\Intervenant_manquant.png"

                    # --- Sécurité Biographie (Tronquer si trop long) ---
                    #if isinstance(bio, str) and len(bio) > 150:
                    #    bio = bio[:147] + "..."
                    #elif pd.isna(bio) or bio == "nan":
                    #    bio = "Aucune biographie disponible pour cet intervenant."
                    
                 
                    # Affchage en ligne (image à droite gauche, nom + Bio à droite)
                    c_img,c_txt = st.columns([1,2])
                    # Affichage
                    with c_img:
                        st.image(img_url, use_container_width=True)

                    with c_txt:
                        bio = actor['biography'] if 'biography' in actor else "Biographie non disponible."
                        if pd.isna(bio) or str(bio).lower() == "nan":
                            bio = "Aucune biographie disponible pour cet intervenant."
                        st.markdown(f"""
                            <div style="color: white; line-height: 1.3;padding-right: 40px;">
                                <b style="font-size: 50px; color: #FFD700;text-shadow: 2px 2px 4px #000000;font-family: 'Great Vibes', cursive; ">{nom_acteur}</b><br>
                                <div style="font-size: 20px; color: white;text-align: justify; margin-top: 5px;text-shadow: 1px 1px 3px #000000;background-color: rgba(0, 0, 0, 0.3); padding: 5px; border-radius: 5px;height: 250px;overflow-y: scroll;display: block;">
                                    {bio}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('<div style="margin-bottom: 25px; border-bottom: 1px solid rgba(214, 185, 139, 0.2);"></div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:gray; text-align:center;">Aucun intervenant répertorié</p>', unsafe_allow_html=True)
