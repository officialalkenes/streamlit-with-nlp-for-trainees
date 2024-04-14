
import nltk
import spacy
nltk.download('stopwords')
spacy.load('en_core_web_sm')
import os
import pandas as pd
import streamlit as st
from pyresparser import ResumeParser


def parse_resume(file):
    if not os.path.exists(file):
        return "Not Found"
    data = ResumeParser(file).get_extracted_data()
    return data


st.title("Streamlit Resume Builder")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type=['pdf'])
if uploaded_file is not None:
    with open(os.path.join("pdf_dir", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    pdf_file_path = os.path.join("pdf_dir", uploaded_file.name)

    # Parse the resume
    data = parse_resume(pdf_file_path)
    
    if data:
        st.write('Parsed Resume Data: ')
        st.json(data)
    else:
        st.error("Failed to parse the resume.")

    os.remove(pdf_file_path)