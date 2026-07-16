import pandas as pd
import streamlit as st

st.title("CSV Viewer")
st.write("Upload a CSV file to display its contents.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        dataframe = pd.read_csv(uploaded_file)
        st.subheader("Preview")
        st.dataframe(dataframe)
    except Exception as error:
        st.error(f"Could not read the CSV file: {error}")