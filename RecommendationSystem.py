
import numpy as np
import pandas as pd
pip install scikit-learn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

movie_title= pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")


movie_title.head(5)
movies=movie_title.merge(credits,on='title')

movies = movies[['movie_id','genres','overview','keywords','title','cast','crew']]

def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movies['cast']=movies['cast'].apply(convert3)

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
    return L


movies['crew']=movies['crew'].apply(fetch_director)

movies_backup=movies.copy()


movies.isna().sum()
movies.dropna(inplace=True)

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
#movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
#movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
movies.head()


movies['overview']=movies['overview'].apply(lambda x:" ".join(x))
movies['overview']=movies['overview'].apply(lambda x:x.lower())

movies['genres']=movies['genres'].apply(lambda x:" ".join(x))
movies['genres']=movies['genres'].apply(lambda x:x.upper())

movies['cast']=movies['cast'].apply(lambda x:" ".join(x))
movies['cast']=movies['cast'].apply(lambda x:x.upper())

movies['keywords']=movies['keywords'].apply(lambda x:" ".join(x))
movies['keywords']=movies['keywords'].apply(lambda x:x.upper())

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')

vector = cv.fit_transform(movies['tags']).toarray()
vector.shape

similarity = cosine_similarity(vector)
movies[movies['title'] == 'The Lego Movie'].index[0]


def recommend(movie, movies, similarity_matrix, search_type=None):
    if search_type == 'title':
        search_column = 'title'
    elif search_type == 'genres':
        search_column = 'genres'
    elif search_type == 'cast':
        search_column = 'cast'
    elif search_type == 'crew':
        search_column = 'crew'
    else:
        print("Invalid search type.")
        return

    matching_movies = movies[movies[search_column].str.contains(movie, case=False)]
    if matching_movies.empty:
        print("No movies found matching the search term.")
        return

    index = matching_movies.index[0]
    distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(movies.iloc[i[0]]['title'])


import pickle

pickle.dump(movies,open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
