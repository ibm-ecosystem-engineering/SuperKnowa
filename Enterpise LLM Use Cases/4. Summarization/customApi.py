from dash import dcc
import os
import requests
import json
from markdownify import markdownify as md

# Your API Endpoint -- below is just example
CUSTOM_API_URL = "https://workbench-api.res.ibm.com/v1/generate"

# Your CUSTOM_API_KEY as an environment variable
CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY", default="")

# Update headers as per need
CUSTOM_API_HEADERS = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(CUSTOM_API_KEY)
    }

# text = user input from the text area,
# custom_payload_json = your payload file as provided in app-config
def custom_api_fn(text, custom_payload_json, type):
    
    # Add user-input to your payload, update code as per your need
    custom_payload_json['inputs'] = [text]

    print(f"calling Custom API call on {CUSTOM_API_URL}")

    # Make POST request
    response_api = requests.post(CUSTOM_API_URL, headers=CUSTOM_API_HEADERS, data=json.dumps(custom_payload_json))
    
    # Convert response to Json
    response_api_json = response_api.json()

    # Add your logic here to extract the data to be shown on screen and return the same
    # 
    op = response_api_json['results'][0]['generated_text']

    return dcc.Markdown(md(op))