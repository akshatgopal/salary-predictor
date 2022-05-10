import streamlit as st
from predict import show_predict
from explore import show_explore_page

page = st.sidebar.selectbox("Explore of Predict", ("Predict", "Explore"))
if page == "Predict":
    show_predict()
else:
    show_explore_page()
