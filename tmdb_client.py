import requests
import streamlit as st

TMDB_BASE      = "https://api.themoviedb.org/3"
POSTER_BASE    = "https://image.tmdb.org/t/p/w500"
POSTER_DEFAULT = None


@st.cache_data(show_spinner=False, ttl=86400)
def fetch_movie_details(tmdb_id, api_key: str) -> dict:
    if not tmdb_id or api_key == "VOTRE_CLE_ICI":
        return _empty_details()
    try:
        tmdb_id = int(tmdb_id)
    except Exception:
        return _empty_details()

    url    = f"{TMDB_BASE}/movie/{tmdb_id}"
    params = {"api_key": api_key, "language": "fr-FR"}

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "poster_url"  : POSTER_BASE + data["poster_path"] if data.get("poster_path") else None,
            "overview"    : data.get("overview", ""),
            "release_date": data.get("release_date", "")[:4] if data.get("release_date") else "?",
            "vote_average": round(data.get("vote_average", 0), 1),
            "tagline"     : data.get("tagline", ""),
        }
    except Exception:
        return _empty_details()


def _empty_details() -> dict:
    return {
        "poster_url"  : None,
        "overview"    : "",
        "release_date": "?",
        "vote_average": 0.0,
        "tagline"     : "",
    }
