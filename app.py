import streamlit as st
import pickle
import pandas as pd
import requests
import os

import time

# styling comes first
st.set_page_config(page_title='Movie Recommender', layout='wide')

page_styles = """
<style>
:root {
  --bg-start: #05060d;
  --bg-end: #101b3a;
  --card: #141c36;
  --card-alt: #1a2550;
  --text: #e6e9ff;
  --accent: #37b6ff;
  --accent-2: #8054ff;
  --muted: #99a4c4;
}

.stApp {
  background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
  color: var(--text);
  font-family: 'Inter', 'Poppins', sans-serif;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 1rem 0.5rem;
}

.app-title { font-size: 2.1rem; font-weight: 800; letter-spacing: 0.02em; color: #ffffff; }

.nav-menu a {
  color: rgba(255,255,255,0.85);
  margin-left: 1.4rem;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
}

.nav-menu a:hover { color: var(--accent); }

#title-block {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
}

#title-block span { color: var(--accent); background: rgba(55,182,255,0.16); padding: 0.12rem 0.4rem; border-radius: 6px; font-size: 0.9rem; }

.card {
  background: linear-gradient(180deg, var(--card) 0%, var(--card-alt) 80%);
  border-radius: 18px;
  border: 1px solid rgba(175,187,255,0.18);
  box-shadow: 0 16px 32px rgba(11, 15, 36, 0.54);
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-6px);
  border-color: rgba(58, 148, 255, 0.75);
  box-shadow: 0 22px 44px rgba(8, 14, 45, 0.70);
}

.card img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}

.card .title { color: #fff; font-size: 1.0rem; font-weight: 700; margin: 0.7rem 0.75rem 0.2rem; }
.card .sub { color: var(--muted); margin: 0 0.75rem 0.85rem; font-size: 0.83rem; }

.select-zone {
  background: rgba(18, 24, 51, 0.90);
  border: 1px solid rgba(70, 103, 190, 0.40);
  border-radius: 16px;
  padding: 14px;
  margin-bottom: 1rem;
}

.stSelectbox > div > div {
  background: rgba(14, 19, 44, 0.95);
  color: #fff;
  border-radius: 12px;
  border: 1px solid rgba(75, 117, 205, 0.5);
}

.recommend-btn .stButton>button {
  margin-top: 0.8rem;
  border-radius: 12px;
  border: none;
  padding: 0.62rem 1.1rem;
  background: linear-gradient(100deg, var(--accent), var(--accent-2));
  color: #fff;
  font-weight: 800;
  letter-spacing: 0.02em;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.recommend-btn .stButton>button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(55, 182, 255, 0.45);
}

.footer { text-align: center; color: rgba(154, 170, 206, 0.8); margin-top: 1.6rem; margin-bottom: 0.6rem; font-size: 0.85rem; }

.footer a { color: rgba(133, 183, 255, 0.8); text-decoration: none; margin: 0 .4rem; }

@media(max-width: 768px) {
  .app-header { flex-direction: column; align-items: flex-start; }
  .app-title { font-size: 1.8rem; }
}
</style>
"""

st.markdown(page_styles, unsafe_allow_html=True)

# layout
col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<div class="app-title">Movie Recommender</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="nav-menu"><a href="#">Home</a><a href="#">About</a></div>', unsafe_allow_html=True)

# Load helpers and data

def fetch_poster(movie_id):
    try:
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=b23722a5b4750197c9d17939caf3848c&language=en-US'.format(movie_id),
            timeout=10
        )
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500/000000/ffffff?text=No+Image"
    except Exception:
        return "https://via.placeholder.com/500/000000/ffffff?text=No+Image"



def recommend_movie(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = int(movies.iloc[i[0]].movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


def load_pickle(filename):
    if not os.path.exists(filename):
        st.error(f"Required file not found: {filename}. Run `python main.py` to generate data and restart the app.")
        st.stop()
    with open(filename, 'rb') as f:
        return pickle.load(f)

movies_dict = load_pickle('movies_dict.pkl')
movies = pd.DataFrame(movies_dict)
similarity = load_pickle('similarity.pkl')

# suggestion selectbox only
movie_titles = movies['title'].tolist()

selected_movie = st.selectbox('Choose movie', movie_titles, key='movie_select')

if st.button('Recommend', key='recommend_button', help='Click to get recommendations'):
    if not selected_movie:
        st.warning('Please select a valid movie title first.')
    else:
        with st.spinner('Generating recommendations...'):
            names, posters = recommend_movie(selected_movie)
        if not names:
            st.info('No movies found. Try a different title.')
        else:
            max_items = len(names)
            grid_cols = st.columns(2 if max_items < 4 else 5)
            for i, c in enumerate(grid_cols):
                if i < len(names):
                    c.markdown(f"<div class='card'><img src='{posters[i]}' alt='poster'><div class='title'>{names[i]}</div><div class='sub'>Recommendation score: {round(0.9 - i*0.1, 2)}</div></div>", unsafe_allow_html=True)

st.markdown('<div class="footer">Made by Ishan Kundra · <a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="#">Contact</a></div>', unsafe_allow_html=True)
