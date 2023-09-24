import main
import streamlit as st 


movie_list  = main.recommend('Avatar')
print(movie_list)

st.title("Movie Recommender System")

movie_name = st.text_input("Movie Name ")


movie_list  = main.recommend(movie_name)

st.dataframe(movie_list)
