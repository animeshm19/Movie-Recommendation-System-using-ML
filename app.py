import streamlit as st
import pickle

movies_list = pickle.load(open('movies.pkl','rb'))
movies_list = movies_list['title'].values

st.title("Move Recommender System")

selected_movie_name = st.selectbox("How would you like to be contacted?",movies_list)

if st.button('Recommend'):
    st.write(selected_movie_name)
