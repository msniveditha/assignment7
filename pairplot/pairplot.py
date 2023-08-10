import streamlit as st
from pathlib import Path
import pandas as pd
import requests
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

description = """
Application to explore the numerical columns as a pair plot.
"""

def get_datasets():
    datasets = root.glob("*.csv")
    return list(datasets)

def get_cat_columns(df):
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()
    cat_cols_fil = [cat_col for cat_col in cat_cols if df[cat_col].nunique()<10]
    return cat_cols_fil

def save_file(newfile_path, file_data):
    data = file_data.getvalue()
    newfile_path.write_bytes(data)

root = Path("datasets")
if not os.path.exists(root):
    os.makedirs(root)

datasets = get_datasets()
label_upload= "Upload a New Dataset"

with st.sidebar:
    st.title("Pair Plot")
    st.markdown(description)

    st.markdown("## Select a Dataset")
    options = [label_upload] + datasets
    path = st.selectbox(label_upload, options)
    if path != label_upload:
        df = pd.read_csv(path)
        categorical_columns = ["None"]+get_cat_columns(df)
        colorby = st.selectbox("Color By", categorical_columns)

if path == label_upload:
    st.markdown("# Upload a New Dataset")
    uploaded_file = st.file_uploader("Upload a CSV file", type="CSV")
    if uploaded_file is not None:
        newfile = root.joinpath(uploaded_file.name)
        if not newfile in datasets:
            save_file(newfile, uploaded_file)
            st.experimental_rerun()
else:
    st.markdown("# Pair Plot")
    if colorby=="None":
        sns_plot = sns.pairplot(data=df)
    else:
        sns_plot = sns.pairplot(data=df,hue=colorby)
    st.pyplot(sns_plot)
