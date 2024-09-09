import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import docx2txt

from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def input_docx_text(uploaded_file):
    if uploaded_file is not None:
        text = docx2txt.process(uploaded_file)
        return text
    else:
        raise FileNotFoundError('file not uploaded')

# Prompt Template
input_prompt = """
hey act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst
and big data engineer. Your task is to extract the following details from the resume:
- Name
- Phone no.
- Email Id
- Job Title
- Current Company
- Skills
- Location

resume:{text}

I want the response in one single string having the structure
{{
Name:, 
Phone no.:, 
Email id:, 
Job Title:,
Current Company:,
Skills:[]
Location
}}
if any detail is not present in the uploaded file then skip that feature"""

# Streamlit app
st.title("Smart ATS")
uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf","docx"])
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            text = input_pdf_text(uploaded_file)
            formatted_prompt = input_prompt.format(text=text)
            response = get_gemini_response(formatted_prompt)

        elif uploaded_file.name.endswith(".docx"):
            text = input_docx_text(uploaded_file)
            formatted_prompt = input_prompt.format(text=text)
            response = get_gemini_response(formatted_prompt)
    else:
        st.write('an error occured')
        
        # formatted_prompt = input_prompt.format(text=text)
        # response = get_gemini_response(formatted_prompt)
    st.subheader(response)