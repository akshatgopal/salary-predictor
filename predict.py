import streamlit as st
import numpy as np
import pickle


def load_model():
    with open("save_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor = data["model"]
le = data["le"]
le_c = data["le_c"]


def show_predict():
    st.title("Software Developer Salary Prediction")
    st.caption(
        "This is a salary prediction model made by using Stack Overflow Developer Survey dataset."
    )
    st.write("### We need some information to predict to salary")
    countries = {
        "Sweden",
        "India",
        "Spain",
        "Germany",
        "Turkey",
        "Canada",
        "France",
        "Switzerland",
        "United Kingdom of Great Britain and Northern Ireland",
        "Russian Federation",
        "Israel",
        "United States of America",
        "Brazil",
        "Italy",
        "Netherlands",
        "Poland",
        "Australia",
        "Norway",
    }

    education = {
        "Post Grad",
        "Master’s degree",
        "Bachelor’s degree",
        "Less than a Bachelors",
    }

    country = st.selectbox("Country", countries)
    edc = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, edc, experience]])
        X[:, 0] = le_c.transform(X[:, 0])
        X[:, 1] = le.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
