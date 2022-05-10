from cProfile import label
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def short(categories, cut):
    cm = {}
    for i in range(len(categories)):
        if categories.values[i] >= cut:
            cm[categories.index[i]] = categories.index[i]
        else:
            cm[categories.index[i]] = "Other"
    return cm


def cexp(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)


def ced(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post Grad"
    return "Less than a Bachelors"


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)
    country_map = short(df["Country"].value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[(df["Salary"] <= 250000) & (df["Salary"] >= 10000)]
    df = df[df["Country"] != "Other"]
    df["YearsCodePro"] = df["YearsCodePro"].apply(cexp)
    df["EdLevel"] = df["EdLevel"].apply(ced)

    return df


df = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2021 """)

    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()

    ax1.pie(data, labels=data.index, startangle=90)
    ax1.axis("equal")

    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    df.boxplot("Salary", "Country", ax=ax)
    plt.suptitle("Salary (US$) vs Country")
    plt.title("")
    plt.ylabel("Salary")
    plt.xticks(rotation=90)

    st.write("""### Number of Data from different countries""")
    st.pyplot(fig1)
    st.write("""### Salary (US$) vs Country""")
    st.pyplot(fig)

    st.write("""#### Mean Salary Based on Country""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary Based on Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
