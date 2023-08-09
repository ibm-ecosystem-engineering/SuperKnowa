# conda create -n ak_docUnderstanding python=3.10 anaconda
# conda activate ak_docUnderstanding
# pip install ipykernel
# python -m ipykernel install --user --name ak_docUnderstanding --display-name "ak_docUnderstanding"
# pip install streamlit
# pip install PdfReader
# pip install requests | tail -n 1
# pip install wget | tail -n 1
# pip install ibm-cloud-sdk-core | tail -n 1
# pip install evaluate | tail -1
#!python3.10 -m pip install PyPDF2
import PyPDF2
import streamlit as st
import pandas as pd
import numpy as np
import base64
from pathlib import Path
import streamlit as st
import os, getpass, wget, json
import requests
from ibm_cloud_sdk_core import IAMTokenManager
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, BearerTokenAuthenticator
from pandas import read_csv

endpoint_url = "https://us-south.ml.cloud.ibm.com"

class Prompt:
    def __init__(self, access_token, project_id):
        self.access_token = access_token
        self.project_id = project_id

    def generate(self, input, model_id, parameters):
        wml_url = f"{endpoint_url}/ml/v1-beta/generation/text?version=2023-05-28"
        Headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "model_id": model_id,
            "input": input,
            "parameters": parameters,
            "project_id": self.project_id
        }
        response = requests.post(wml_url, json=data, headers=Headers)
        if response.status_code == 200:
            return response.json()["results"][0]
        else:
            return response.text
        
access_token = IAMTokenManager(
    apikey = "ADD YOUR API KEY HERE",
    url = "https://iam.cloud.ibm.com/identity/token"
).get_token()

project_id = "ADD YOUR PROJECT ID HERE"


#model_id = "google/flan-ul2"
model_id = "google/flan-t5-xxl"

parameters = {
         "decoding_method": "greedy",
         "min_new_tokens": 1,
         "max_new_tokens": 500
}

prompt = Prompt(access_token, project_id)



def extract_text_from_pdf(pdf_file_path):
    if(pdf_file_path=="doc1.pdf"):
        return """
                "ABC Retail Store
                123 Main Street
                City, State, ZIP
                Phone: (555) 123-4567

                INVOICE

                Invoice No: INV-2023-001
                Date: 2023-07-15

                Bill To:
                John Doe
                456 Park Avenue
                City, State, ZIP

                | Item         | Quantity | Price   | Total   |
                |--------------|----------|---------|---------|
                | Product A    | 2        | $10.00  | $20.00  |
                | Product B    | 1        | $15.00  | $15.00  |
                | Product C    | 3        | $8.00   | $24.00  |

                Total: $59.00"
                """
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        combined_text = ""
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            combined_text += text

        return combined_text
    
st.title('PDF Understanding (powered by watsonx)')
#st.write("Select the file to be analysed:")
#st.write(selection)
inputFile = st.selectbox(
    'File to be analysed:',
    (['doc1.pdf','doc2.pdf','doc3.pdf']))

pdf_path = Path(inputFile)
base64_pdf = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="500px" type="application/pdf"></iframe>
"""
st.markdown(pdf_display, unsafe_allow_html=True)

# Extracting text from pdf
pdf_path = inputFile
extractedText = extract_text_from_pdf(pdf_path)
print(extractedText)

document =  f"""{extractedText}"""
import time

question1 = "\nWhat type of document is it?\n"
result1 = prompt.generate(" ".join([document,question1]), model_id, parameters)['generated_text']
time.sleep(1)
question2 = "\nExtract key information from the document above.\n"
result2 = prompt.generate(" ".join([document,question2]), model_id, parameters)['generated_text']
time.sleep(1)   
# question3  = "\nextract key value pairs from the document above\n"
# result3 = prompt.generate(" ".join([document,question3]), model_id, parameters)['generated_text']

# question4 = """\nExtract detailed information from the document above.\n"""
# result4 = prompt.generate(" ".join([document,question4]), model_id, parameters)['generated_text']
#st.markdown("""---""")
st.divider()

#
st.write("The type of document is : ",result1)
st.write("Key Information in this document : ",result2)
#st.write("Details : ",result4)

#st.write("DOCUMENT : ",document)

