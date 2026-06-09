import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import gc

DATA_PATH = "C:/Users/hh/Downloads/recomamandation/ml-32m/ml-32m/"

def load_data():
    movies = pd.read_csv(os.path.join(DATA_PATH, "movies.csv"),
                         dtype={"movieId": "int32"})
    links  = pd.read_csv(os.path.join(DATA_PATH, "links.csv"),
                         usecols=["movieId", "tmdbId"],
                         dtype={"movieId": "int32"})

    rating_counts = {}
    rating_sums   = {}
    for chunk in pd.read_csv(
        os.path.join(DATA_PATH, "ratings.csv"),
        usecols=["movieId", "rating"],
        chunksize=100_000,
        dtype={"movieId": "int32", "rating": "float32"}
    ):
        for mid, rating in zip(chunk["movieId"], chunk["rating"]):
            if mid in rating_counts:
                rating_counts[mid] += 1
                rating_sums[mid]   += rating
            else:
                rating_counts[mid]  = 1
                rating_sums[mid]    = rating
        gc.collect()

    popular = pd.DataFrame({
        "movieId"     : list(rating_counts.keys()),
        "rating_count": list(rating_counts.values()),
        "avg_rating"  : [rating_sums[m] / rating_counts[m] for m in rating_counts]
    })
    del rating_counts, rating_sums
    gc.collect()

    top_movies = popular[popular["rating_count"] >= 100].nlargest(1000, "rating_count")
    del popular
    gc.collect()

    tags = pd.read_csv(os.path.join(DATA_PATH, "tags.csv"),
                       usecols=["movieId", "tag"],
                       dtype={"movieId": "int32"})
    tags_grouped = (
        tags.groupby("movieId")["tag"]
        .apply(lambda x: " ".join(x.dropna().astype(str)))
        .reset_index()
    )
    del tags
    gc.collect()

    df = movies[movies["movieId"].isin(top_movies["movieId"])].copy()
    df = df.merge(top_movies,   on="movieId", how="left")
    df = df.merge(tags_grouped, on="movieId", how="left")
    df = df.merge(links,        on="movieId", how="left")   # ← tmdbId

    df["tag"]          = df["tag"].fillna("")
    df["genres_clean"] = df["genres"].str.replace("|", " ", regex=False)
    df["features"]     = df["genres_clean"] + " " + df["tag"]
    df["tmdbId"]       = pd.to_numeric(df["tmdbId"], errors="coerce")
    df = df.reset_index(drop=True)
    return df


def build_similarity_matrix(df):
    tfidf        = TfidfVectorizer(stop_words="english", max_features=2000)
    tfidf_matrix = tfidf.fit_transform(df["features"])
    return cosine_similarity(tfidf_matrix, tfidf_matrix)


def get_recommendations(title, df, cosine_sim, n=10):
    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
    if title not in indices:
        return []
    idx        = indices[title]
    sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n + 1]
    return df.iloc[[i[0] for i in sim_scores]][
        ["title", "genres", "avg_rating", "rating_count", "tmdbId"]
    ].to_dict("records")
