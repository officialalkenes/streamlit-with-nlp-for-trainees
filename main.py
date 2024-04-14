import base64
import os
import pandas as pd
import streamlit as st
from pyresparser import ResumeParser
import nltk
import spacy

# Downloading necessary NLTK resources and loading Spacy model
nltk.download('stopwords')
spacy.load('en_core_web_sm')

# Skill categories dictionary for categorization
skill_categories = {
    'Technical': ['Python', 'Java', 'C++', 'SQL', 'JavaScript'],
    'Soft': ['Communication', 'Teamwork', 'Leadership', 'Time Management'],
    'Analytical': ['Data Analysis', 'Critical Thinking', 'Problem Solving']
}
user_type = ['Normal User', "Admin User"]

def parse_resume(file_path):
    """ Parses the resume and extracts data using ResumeParser. """
    if not os.path.exists(file_path):
        return "File not found"
    
    try:
        data = ResumeParser(file_path).get_extracted_data()
        return {
            'name': data.get('name'),
            'email': data.get('email'),
            'mobile_number': data.get('mobile_number'),
            'skills': data.get('skills'),
            'college_name': data.get('college_name'),
            'degree': data.get('degree'),
            'designation': data.get('designation'),
            'experience': data.get('experience'),
            'total_experience': data.get('total_experience')
        }
    except Exception as e:
        return f"Error parsing the resume: {str(e)}"

def categorize_skills(skills):
    """ Categorizes skills into predefined categories. """
    categorized_skills = {category: [] for category in skill_categories.keys()}
    if skills:
        for skill in skills:
            for category, keywords in skill_categories.items():
                if skill in keywords:
                    categorized_skills[category].append(skill)
    return categorized_skills

def display_info(data, info_selection):
    """ Displays selected information from the parsed resume data. """
    for info in info_selection:
        if info in data and data[info]:
            st.write(f"**{info.replace('_', ' ').title()}:**", data[info])

def handle_file_upload(user):
    """ Handles file upload logic for admin and regular users. """
    with st.sidebar:
        if user == "Admin User":
            uploaded_files = st.file_uploader("Upload multiple resumes", type=['pdf'], accept_multiple_files=True)
            return uploaded_files
        else:
            uploaded_file = st.file_uploader("Upload your resume", type=['pdf'])
            return [uploaded_file] if uploaded_file else []

def main():
    """ Main function to orchestrate the uploading and parsing of resumes. """
    st.title("Streamlit Resume Parser")

    with st.sidebar:
        st.markdown("Choose User")
        user = st.sidebar.selectbox("Pick What type of User you are", user_type)
        info_selection = st.multiselect('Select the information you want to display:',
                                        ['Email', 'Mobile Number', 'Skills', 'Education', 'Experience'],
                                        default=['Skills', 'Experience'])
    
    uploaded_files = handle_file_upload(user)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file is not None:
                # Assuming a secure way to save and handle files
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                data = parse_resume(uploaded_file.name)
                if isinstance(data, dict):
                    display_info(data, info_selection)
                else:
                    st.error(data)

                os.remove(uploaded_file.name)  # Clean up the uploaded file

main()
