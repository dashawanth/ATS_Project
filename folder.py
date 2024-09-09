# import streamlit as st
# import google.generativeai as genai
# import os
# import PyPDF2 as pdf
# import pandas as pd
# import docx2txt
# import json
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv

# load_dotenv()  # Load all the environment variables

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Folder path containing resumes
# folder_path = "D:/ATS/resumes"

# # Gemini Pro Response
# def get_gemini_response(input):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(input)
#     return response.text

# def input_pdf_text(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# def input_docx_text(uploaded_file):
#     doc = docx2txt.Document(uploaded_file)
#     text = ""
#     for para in doc.paragraphs:
#         text += para.text + "\n"
#     return text

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
# {{
# Name:,
# Phone no.:,
# Email id:,
# Job Title:,
# Current Company:,
# Skills:[],
# Location:
# }}
# if any detail is not present in the uploaded file then skip that feature"""

# # Initialize an empty list to store the extracted details
# data = []

# # Streamlit app
# st.title("Smart ATS")
# folder_path = st.text_input("Enter the folder path containing resumes")

# submit = st.button("Submit")

# if submit:
#     if folder_path:
#         data = []
#         # Iterate through the files in the folder
#         for filename in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, filename)
#             if filename.endswith('.pdf'):
#                 text = input_pdf_text(file_path)
#             elif filename.endswith('.docx'):
#                 text = input_docx_text(file_path)
#             else:
#                 continue

#             formatted_prompt = input_prompt.format(text=text)
#             response = get_gemini_response(formatted_prompt)

#             # Append the parsed data to the data list
#             data.append(response)

#         # Create a DataFrame and save to CSV
#         df = pd.DataFrame(data)
#         df.to_csv('resumes_details.csv', index=False)

#         st.success("Resumes processed and saved to resumes_details.csv")
#     else:
#         st.error("Please enter a valid folder path.")

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import pandas as pd
import docx2txt
import json
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import re  # For regular expression-based data validation

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Folder path containing resumes
folder_path = "D:/ATS/resumes"

# Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        print(f"Error processing input: {e}")
        return None

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def input_docx_text(uploaded_file):
    text = docx2txt.process(uploaded_file)
    # text = ""
    # for para in doc.paragraphs:
    #     text += para.text + "\n"
    return text

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
Skills:[],
Location:
if any detail is not present in the uploaded file then skip that feature"""

# Initialize an empty list to store the extracted details
data = []

# Streamlit app
st.title("Smart ATS")
folder_path = st.text_input("Enter the folder path containing resumes")

submit = st.button("Submit")

if submit:
    if folder_path:
        data = []
        # Iterate through the files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if filename.endswith('.pdf') or filename.endswith('.docx'):
                try:
                    if filename.endswith('.pdf'):
                        text = input_pdf_text(file_path)
                    elif filename.endswith('.docx'):
                        text = input_docx_text(file_path)

                    formatted_prompt = input_prompt.format(text=text)
                    response = get_gemini_response(formatted_prompt)

                    # Replace single quotes with double quotes (if necessary)
                    response = re.sub(r"'", '"', response)

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
