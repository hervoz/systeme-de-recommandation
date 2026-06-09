import streamlit as st
from recommender import load_data, build_similarity_matrix, get_recommendations
from tmdb_client import fetch_movie_details

# ── Config ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MovieHub",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .moviehub-logo {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
  }
  .moviehub-logo h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 80px;
    font-weight: 900;
    letter-spacing: -2px;
    color: #E8000A;
    -webkit-text-stroke: 1.5px #B00007;
    margin: 0;
    line-height: 1;
  }
  .moviehub-logo .bar {
    width: 420px;
    height: 4px;
    background: #E8000A;
    border-radius: 2px;
    margin: 6px auto;
    opacity: 0.85;
  }
  .moviehub-logo .tagline {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
    letter-spacing: 8px;
    color: #888;
    margin-top: 4px;
  }
</style>

<div class="moviehub-logo">
  <h1>MOVIEHUB</h1>
  <div class="bar"></div>
  <p class="tagline">DISCOVER · WATCH · ENJOY</p>
</div>
""", unsafe_allow_html=True)


# ── Style Netflix-inspired ────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');

  .stApp { background-color: #141414; color: #e5e5e5; font-family: 'Inter', sans-serif; }
  h1,h2,h3 { color: #E50914 !important; }
  [data-testid="stSidebar"] { background-color: #1a1a1a; }
  div[data-testid="stMetricValue"] { color: #E50914 !important; }
  div[data-testid="stMetricLabel"] { color: #aaa !important; }

  .site-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    color: #E50914 !important;
    letter-spacing: 2px;
    line-height: 1;
    margin-bottom: 0;
  }
  .site-subtitle {
    font-size: 0.95rem;
    color: #888;
    margin-top: 4px;
    margin-bottom: 20px;
  }

  .movie-card {
    background: #1f1f1f;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 16px;
    border: 1px solid #2a2a2a;
    transition: transform .2s ease, box-shadow .2s ease;
  }
  .movie-card:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 30px rgba(229,9,20,.35);
  }
  .movie-card img {
    width: 100%;
    display: block;
    border-radius: 10px 10px 0 0;
  }
  .movie-card-placeholder {
    width: 100%;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5rem;
    border-radius: 10px 10px 0 0;
  }
  .movie-info { padding: 10px 12px 14px; }
  .movie-title-card {
    font-size: 0.88rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
    line-height: 1.3;
  }
  .movie-meta { font-size: 0.75rem; color: #aaa; margin-bottom: 6px; }
  .genre-badge {
    display: inline-block;
    background: #E50914;
    color: #fff;
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 0.65rem;
    margin: 2px 2px 2px 0;
  }
  .overview-text {
    font-size: 0.75rem;
    color: #bbb;
    line-height: 1.45;
    margin-top: 6px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .rank-badge {
    position: absolute;
    top: 8px;
    left: 8px;
    background: rgba(0,0,0,.75);
    color: #E50914;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.8rem;
    font-weight: 800;
  }
</style>
""", unsafe_allow_html=True)


   
# ── Clé TMDB ─────────────────────────────────────────────────────────────────
try:
    TMDB_API_KEY = st.secrets["tmdb"]["api_key"]
except Exception:
    TMDB_API_KEY = "1e07da69a28266484b243ae890f8e699"

# ── Genre styles ──────────────────────────────────────────────────────────────
GENRE_STYLE = {
    "Action": {"color": "#E50914", "emoji": "💥"},
    "Adventure": {"color": "#F5A623", "emoji": "🗺️"},
    "Animation": {"color": "#50E3C2", "emoji": "🎨"},
    "Children": {"color": "#B8E986", "emoji": "🧸"},
    "Comedy": {"color": "#D4AC0D", "emoji": "😂"},
    "Crime": {"color": "#4A4A4A", "emoji": "🔫"},
    "Documentary": {"color": "#7B68EE", "emoji": "🎙️"},
    "Drama": {"color": "#9B59B6", "emoji": "🎭"},
    "Fantasy": {"color": "#1ABC9C", "emoji": "🧙"},
    "Film-Noir": {"color": "#2C3E50", "emoji": "🕵️"},
    "Horror": {"color": "#922B21", "emoji": "👻"},
    "Musical": {"color": "#E91E8C", "emoji": "🎵"},
    "Mystery": {"color": "#5D6D7E", "emoji": "🔍"},
    "Romance": {"color": "#E74C8B", "emoji": "❤️"},
    "Sci-Fi": {"color": "#2980B9", "emoji": "🚀"},
    "Thriller": {"color": "#E67E22", "emoji": "😱"},
    "War": {"color": "#784212", "emoji": "⚔️"},
    "Western": {"color": "#CA6F1E", "emoji": "🤠"},
}
DEFAULT_STYLE = {"color": "#555", "emoji": "🎬"}

def primary_genre(genres_str):
    for g in genres_str.split("|"):
        if g in GENRE_STYLE:
            return g
    return None

# ── Chargement ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=" Chargement du dataset MovieLens…")
def init():
    df         = load_data()
    cosine_sim = build_similarity_matrix(df)
    return df, cosine_sim

df, cosine_sim = init()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("##  Paramètres")
    n_reco       = st.slider("Nombre de recommandations", 5, 20, 10)
    all_genres   = sorted({g for gs in df["genres"].str.split("|") for g in gs if g != "(no genres listed)"})
    genre_filter = st.multiselect(" Filtrer par genre", all_genres)
    min_rating   = st.slider(" Note minimale", 0.0, 5.0, 3.0, 0.5)
    show_overview = st.toggle(" Afficher les synopsis", value=True)

    st.divider()
    st.metric("Films indexés", f"{len(df):,}")
    st.metric("Algorithme",    "Cosine Similarity")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .netflix-header {
    text-align: center;
    padding: 2rem 0 1rem;
  }
  .netflix-header .eyebrow {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 11px;
    letter-spacing: 7px;
    color: #E8000A;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .netflix-header h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -1px;
    color: #E8000A;
    -webkit-text-stroke: 1px #900005;
    margin: 0;
    line-height: 1.1;
  }
  .netflix-header .bar {
    width: 180px;
    height: 3px;
    background: #E8000A;
    border-radius: 2px;
    margin: 10px auto 12px;
    opacity: 0.9;
  }
  .netflix-header .subtitle {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 11px;
    letter-spacing: 3.5px;
    color: #888;
    text-transform: uppercase;
  }
</style>

<div class="netflix-header">
  <p class="eyebrow"> &nbsp; </p>
  <h1>Recommandation de Films</h1>
  <div class="bar"></div>
  <p class="subtitle">Cosine Similarity &nbsp;·&nbsp; MovieLens 32M &nbsp;·&nbsp; TMDB</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Sélection ─────────────────────────────────────────────────────────────────
movie_list     = df["title"].sort_values().tolist()
selected_movie = st.selectbox(" Choisis un film :", movie_list)

# Aperçu film sélectionné
if selected_movie:
    row     = df[df["title"] == selected_movie].iloc[0]
    tmdb_id = row.get("tmdbId")
    details = fetch_movie_details(tmdb_id, TMDB_API_KEY)
    pg      = primary_genre(row["genres"])
    style   = GENRE_STYLE.get(pg, DEFAULT_STYLE)
    genres  = row["genres"].split("|")
    badges  = " ".join([f'<span class="genre-badge">{g}</span>' for g in genres])

    c1, c2 = st.columns([1, 3])
    with c1:
        if details["poster_url"]:
            st.image(details["poster_url"], use_container_width=True)
        else:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{style['color']}cc,{style['color']}33);
                        border-radius:10px;height:260px;display:flex;align-items:center;
                        justify-content:center;font-size:5rem">
              {style['emoji']}
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"## {selected_movie}")
        if details.get("tagline"):
            st.markdown(f"*{details['tagline']}*")
        st.markdown(badges, unsafe_allow_html=True)
        st.markdown(
            f" **{details['release_date']}** &nbsp;|&nbsp; "
            f"Notes : **{details['vote_average']}/10** (TMDB) &nbsp;|&nbsp; "
            f" **{row['avg_rating']:.2f}/5** MovieLens · {int(row['rating_count']):,} votes",
            unsafe_allow_html=True
        )
        if show_overview and details.get("overview"):
            st.markdown(f"_{details['overview']}_")

col_btn, _ = st.columns([1, 5])
with col_btn:
    search = st.button(" Recommander", use_container_width=True)

st.divider()

# ── Résultats ─────────────────────────────────────────────────────────────────
if search:
    raw = get_recommendations(selected_movie, df, cosine_sim, n=n_reco * 4)
    if genre_filter:
        raw = [r for r in raw if any(g in r["genres"] for g in genre_filter)]
    raw     = [r for r in raw if r["avg_rating"] >= min_rating]
    results = raw[:n_reco]

    if not results:
        st.warning(" Aucun résultat. Essaie d'assouplir les filtres.")
    else:
        st.subheader(f" {len(results)} films similaires à **{selected_movie}**")
        cols = st.columns(5)
        for i, movie in enumerate(results):
            details = fetch_movie_details(movie["tmdbId"], TMDB_API_KEY)
            pg      = primary_genre(movie["genres"])
            style   = GENRE_STYLE.get(pg, DEFAULT_STYLE)
            genres  = movie["genres"].split("|")
            badges  = " ".join([f'<span class="genre-badge">{g}</span>' for g in genres[:3]])

            with cols[i % 5]:
                poster_html = (
                    f'<img src="{details["poster_url"]}" alt="{movie["title"]}"/>'
                    if details["poster_url"] else
                    f'<div class="movie-card-placeholder" style="background:linear-gradient(135deg,{style["color"]}cc,{style["color"]}33)">{style["emoji"]}</div>'
                )
                overview_html = (
                    f'<div class="overview-text">{details["overview"]}</div>'
                    if show_overview and details.get("overview") else ""
                )
                st.markdown(f"""
                <div class="movie-card" style="position:relative">
                  {poster_html}
                  <span class="rank-badge">#{i+1}</span>
                  <div class="movie-info">
                    <div class="movie-title-card">{movie['title']}</div>
                    <div class="movie-meta">
                      Notes : {movie['avg_rating']:.2f}/5 · {int(movie['rating_count']):,} votes
                    </div>
                    {badges}
                    {overview_html}
                  </div>
                </div>
                """, unsafe_allow_html=True)
                