import pickle, pandas as pd
movies = pd.DataFrame(pickle.load(open('movies_dict.pkl','rb')))
print('total', len(movies))
print(movies['title'].head(30).tolist())
print('Harry occurrences:', sum('Harry' in t for t in movies['title']))
