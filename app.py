from dotenv import load_dotenv
import os
import pickle
import streamlit as st
import requests
import pandas as pd
import time

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
# --- Fetch poster safely with retry and fallback ---
def fetch_poster(movie_id, retries=3):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            else:
                return "https://via.placeholder.com/300x450?text=No+Poster"
        except Exception as e:
            if attempt == retries - 1:
                st.warning(f"Could not fetch poster for movie ID {movie_id}: {e}")
                return "https://via.placeholder.com/300x450?text=Error"
            time.sleep(1)

# --- Recommendation logic with valid movie filtering ---
def recommend(movie):
    matches = movies[movies['title'] == movie]
    if matches.empty:
        st.error("Selected movie not found in the dataset.")
        return [], []

    index = matches.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    count = 0
    for i in distances[1:]:
        if count >= 5:
            break
        try:
            movie_id = movies.iloc[i[0]]['id']
            name = movies.iloc[i[0]]['title']
            poster = fetch_poster(movie_id)
            if poster:  # Ensure it's not empty or None
                recommended_movie_names.append(name)
                recommended_movie_posters.append(poster)
                count += 1
        except Exception as e:
            st.warning(f"⚠️ Skipped a movie due to error: {e}")
            continue

    # Ensure list has exactly 5 items using placeholders
    while len(recommended_movie_names) < 5:
        recommended_movie_names.append("Unavailable")
        recommended_movie_posters.append("https://via.placeholder.com/300x450?text=Not+Available")

    return recommended_movie_names, recommended_movie_posters

# --- Streamlit UI ---
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Convert dict to DataFrame if needed
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# UI elements
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
