# -*- coding: utf-8 -*-
"""movie_recommender.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nwpTEj9xX0KfaXbCLgGwSlB-2S4QARgv
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
movies = pd.read_csv("/content/drive/MyDrive/Movie_Recommendation_System/tmdb_5000_movies.csv")
credits = pd.read_csv("/content/drive/MyDrive/Movie_Recommendation_System/tmdb_5000_credits.csv")
# movies.head(1)
# credits.head(1)['cast'].values
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.head()

movies.isnull().sum()

movies.dropna(inplace=True)

movies.duplicated().sum()

movies.iloc[0].genres

import ast

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
      L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

def convert_top3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert_top3)

movies.head()

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])

movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

newdf = movies[['movie_id', 'title', 'tags']]

newdf['tags'] = newdf['tags'].apply(lambda x:" ".join(x))

newdf.head()

newdf['tags'][0]

newdf['tags'] = newdf['tags'].apply(lambda x:x.lower())

newdf.head()

!pip install nltk

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i)) # if ['love','loved','loving'] will return love i.e the root term
    return " ".join(y)

newdf['tags'] = newdf['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, stop_words = 'english')

vectors = cv.fit_transform(newdf['tags']).toarray()

vectors

cv.get_feature_names_out()

stem('In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. Action Adventure Fantasy ScienceFiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d SamWorthington ZoeSaldana SigourneyWeaver JamesCameron')

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

sorted(list(enumerate(similarity[0])), reverse = True, key = lambda x:x[1])[1:6]

def recommend(movie):
    movie_index = newdf[newdf['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]

    for i in movies_list:
        print(newdf.iloc[i[0]].title)
        # print(i)

recommend('Batman Begins')

newdf.iloc[539]

import pickle

pickle.dump(newdf, open('movies.pkl', 'wb'))

newdf['title'].values

pickle.dump(newdf.to_dict(), open('movie_dict.pkl', 'wb'))

# pickle.dump(newdf.to_dict(), open('movies_dict.pkl', 'wb'))

pickle.dump(similarity, open("similarity.pkl", 'wb'))

