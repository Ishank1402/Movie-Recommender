import pandas as pd
import numpy as np
import ast
import builtins

try:
    import nltk
except ImportError as e:
    raise ImportError("nltk is required for this script. Install with 'pip install nltk'.") from e

np.set_printoptions(threshold=np.inf)

original_print = print

def spaced_print(*args, **kwargs):
    original_print("\n" + "-"*60)
    original_print(*args, **kwargs)
    original_print("-"*60 + "\n")

builtins.print = spaced_print

# Load data
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

print(movies.head(1))
print(credits.head(1)['cast'].values)

# Merge
movies = movies.merge(credits, on='title')

print(movies.shape)
print(movies.head(1))

print(movies['original_language'].value_counts())

print(movies.info())

# Select columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Clean data
movies.dropna(inplace=True)

print(movies.isnull().sum())
print(movies.duplicated().sum())

print(movies.iloc[0].genres)

# Convert functions
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L

movies['genres'] = movies['genres'].apply(convert)
print(movies['genres'])

movies['keywords'] = movies['keywords'].apply(convert)

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter < 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert3)
print(movies['cast'])

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i["name"])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)
print(movies['crew'])

# Overview split
movies['overview'] = movies['overview'].apply(lambda x: x.split())
print(movies['overview'])

# Remove spaces
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

print(movies.head(5))

# Create tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

print(movies.head(2))

# New dataframe
new_df = movies[['movie_id', 'title', 'tags']]

print(new_df.head())
print(new_df['tags'][0])

# Convert list to string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

print(new_df['tags'][0])
print(new_df.head())

# Lowercase
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
print(new_df.head())

# Stemming
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings
embeddings = model.encode(new_df['tags'].tolist())

# Convert to numpy
embeddings = np.array(embeddings).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Build similarity matrix (app uses this)
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(embeddings)

# Save everything
pickle.dump(new_df.to_dict(), open('movies_dict.pkl', "wb"))
pickle.dump(index, open('faiss_index.pkl', "wb"))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

# Recommendation function
def recommend(movie):

# Step 1: Get movie index

    movie_index = new_df[new_df['title'] == movie].index[0]

# Step 2: Get similarity scores
    distances = similarity[movie_index]

# Step 3: sort movies based on similarity
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
# Step 4: Print top 5 movies
    for i in movies_list:
        print(new_df.iloc[i[0]].title)

# Call function
recommend("Avatar")

# Save
import pickle
pickle.dump(new_df.to_dict(), open('movies_dict.pkl', "wb"))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

new_df["title"].values
print(new_df["title"].values[0:5])


