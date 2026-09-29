import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    df = pd.read_csv("output.csv")
    return df

st.title("Decrees Dashboard")

df = load_data()

tab1, tab2, tab3 = st.tabs(["Missing Data Points", "Decrees Per Year", "Categorization"])

with tab1:
    st.header("Missing Data Points")
    # Missing data: rows where Year, ID, or Title is null or empty string
    missing_data = df[df[['Year', 'ID', 'Title']].isnull().any(axis=1) | (df[['Year', 'ID', 'Title']] == "").any(axis=1)]
    if missing_data.empty:
        st.write("No missing data points found in core columns!")
    else:
        st.dataframe(missing_data)

with tab2:
    st.header("Number of Decrees per Year")
    counts_per_year = df['Year'].value_counts().sort_index()
    st.bar_chart(counts_per_year)

with tab3:
    st.header("Categorized Decrees")
    st.write("Below are the decrees categorized using Gemini based on our static classification.")

    # Show value counts of the new Category column
    if 'Category' in df.columns:
        cat_counts = df['Category'].value_counts()
        st.bar_chart(cat_counts)

        # Display the data
        st.dataframe(df[['Year', 'ID', 'Title', 'Category', 'Subcategory', 'Explanation']])
    else:
        st.write("Categorization data is missing. Please run `merge_categories.py`.")
