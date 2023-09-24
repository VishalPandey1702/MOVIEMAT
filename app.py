import main
import streamlit as st 

st.title("Movie Recommender System")

movie_name = st.text_input("Movie Name ")


movie_list  = main.recommend(movie_name)

st.dataframe(movie_list)
