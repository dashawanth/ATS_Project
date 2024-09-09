# import streamlit as st
# import google.generativeai as genai
# import os
# import PyPDF2 as pdf
# import docx2txt
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv

# load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Gemini Pro Response
# def get_gemini_response(input):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(input)
#     return response.text

# def input_pdf_text(uploaded_file):
#     if uploaded_file.endswith(".pdf"):
#         reader = pdf.PdfReader(uploaded_file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#         return text
#     elif uploaded_file.endswith(".docx"):
#         doc = docx2txt.Document(uploaded_file)
#         text = ""
#         for para in doc.paragraphs:
#             text += para.text + "\n"
#         return text
#     else:
#         print("An error occured")

# def process_multiple_files(directory_path):
#     results = []
#     for filename in os.listdir(directory_path):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(directory_path, filename)
#             reader = pdf.PdfReader(file_path)
#             text = ""
#             for page in reader.pages:
#                 text += page.extract_text()
#             return text
#         elif filename.endswith(".docx"):
#             file_path = os.path.join(directory_path, filename)
#             doc = docx2txt.Document(file_path)
#             text = ""
#             for para in doc.paragraphs:
#                 text += para.text + "\n"
#             return text
#         else:
#             print("An error occured")


#             # with open(file_path, 'rb') as f:
#             #     reader = pdf.PdfReader(f)
#             #     text = input_pdf_text(reader)
#         formatted_prompt = input_prompt.format(text=text)
#         response = get_gemini_response(formatted_prompt)
#         results.append(response)
#     return results

# # Prompt Template
# input_prompt = """
# hey act like a skilled or very experienced ATS (Application Tracking System)
# with a deep understanding of tech field, software engineering, data science, data analyst
# and big data engineer. Your task is to extract the following details from the resume:
# - Name
# - Phone no.
# - Email Id
# - Job Title
# - Current Company
# - Skills
# - Location

# resume:{text}

# I want the response in one single string having the structure
# Name:, 
# Phone no.:, 
# Email id:, 
# Job Title:,
# Current Company:,
# Skills:[]
# Location
# if any detail is not present in the uploaded file then skip that feature"""

# # Streamlit app
# st.title("Smart ATS")

# # Add a dropdown option for file selection with "Select Option" as default
# file_selection_option = st.selectbox("Choose File Selection Method", ["Select Option", "Upload File", "Provide File Path"])

# # Check if the user has selected an option other than "Select Option"
# if file_selection_option != "Select Option":
#     if file_selection_option == "Upload File":
#         uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")
#     elif file_selection_option == "Provide File Path":
#         file_path = st.text_input("Enter File Path")

# submit = st.button("Submit")

# if submit:
#     if file_selection_option == "Upload File":
#         text = input_pdf_text(uploaded_file)
#         formatted_prompt = input_prompt.format(text=text)
#         response = get_gemini_response(formatted_prompt)
#         st.subheader(response)
#     elif file_selection_option == "Provide File Path":
#         if file_path:
#             if os.path.isdir(file_path):
#                 responses = process_multiple_files(file_path)
#                 for response in responses:
#                     st.subheader(response)
#             else:
#                 print("An error occured")
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import docx2txt
import pandas as pd
import json
import re

from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

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

def input_pathpdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def input_pathdocx_text(uploaded_file):
    if uploaded_file is not None:
        text = docx2txt.process(uploaded_file)
        return text
    else:
        raise FileNotFoundError('file not uploaded')
    # text = ""
    # for para in doc.paragraphs:
    #     text += para.text + "\n"
    
    
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
Name:, 
Phone no.:, 
Email id:, 
Job Title:,
Current Company:,
Skills:[]
Location
if any detail is not present in the uploaded file then skip that feature"""

# Streamlit app
st.title("Smart ATS")

with st.sidebar:
    file_selection_option = st.radio("Choose File Selection Method", ["Upload File", "Provide Folder Path"])

# Check if the user has selected an option other than "Select Option"
if file_selection_option != "Select Option":
    if file_selection_option == "Upload File":
        uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf","docx"])
    elif file_selection_option == "Provide Folder Path":
        folder_path = st.text_input("Enter File Path")

submit = st.button("Submit")

if submit:
    if file_selection_option == "Upload File":
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
    elif file_selection_option == "Provide Folder Path":
        if folder_path:
            data=[]
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if filename.endswith('.pdf') or filename.endswith('.docx'):
                    try:
                        if filename.endswith('.pdf'):
                            text = input_pathpdf_text(file_path)
                        elif filename.endswith('.docx'):
                            text = input_pathdocx_text(file_path)

                        formatted_prompt = input_prompt.format(text=text)
                        response = get_gemini_response(formatted_prompt)

                        # Replace single quotes with double quotes (if necessary)
                        response = re.sub(r"'", '"', response)
                        response = response.replace('\n', ' ')
                        # Parse the response and validate extracted data
                        parsed_data = json.dumps(response)

                        # Append the parsed data to the data list
                        data.append(parsed_data)
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")

            # Create a DataFrame and save to CSV
            df = pd.DataFrame(data)
            df.to_csv('resumes_details.csv', index=False)

            st.success("Resumes processed and saved to resumes_details.csv")
        else:
            st.error("Please enter a valid folder path.")

    #         if os.path.isdir(folder_path):

    #             responses = process_multiple_files(folder_path)
    #             formatted_prompt = input_prompt.format(text=text)
    #             response = get_gemini_response(formatted_prompt)

    #             # Replace single quotes with double quotes (if necessary)
    #             response = re.sub(r"'", '"', response)

    #             # Parse the response and validate extracted data
    #             parsed_data = json.dumps(response)

    #             # Append the parsed data to the data list
    #             data.append(parsed_data)

    #     # Create a DataFrame and save to CSV
    #     df = pd.DataFrame(data)
    #     df.to_csv('resumes_details.csv', index=False)

    #     st.success("Resumes processed and saved to resumes_details.csv")
    # else:
    #     st.error("Please enter a valid folder path.")