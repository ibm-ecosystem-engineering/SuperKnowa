from bs4 import BeautifulSoup
import re
import requests
import json
import os,pickle
import time
import yaml

#Reading the content of config file
with open("./../config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    cfg = cfg['LLMQnA']

question = cfg['question']
MODEL_AUTH_TOKEN = cfg['MODEL_AUTH_TOKEN']
model_url = cfg['model_url']
model_id = cfg['model_id']
with open (cfg['context'], 'rb') as fp:
    context = pickle.load(fp)


def format_string(doc):
    doc = doc.encode("ascii", "ignore")
    string_decode = doc.decode()
    cleantext = BeautifulSoup(string_decode, "lxml").text
    perfecttext = " ".join(cleantext.split())
    perfecttext = re.sub(' +', ' ', perfecttext).strip('"')
    return perfecttext

def process_watsonx_request():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': MODEL_AUTH_TOKEN,
    }
    
    json_data = {
      "model_id": model_id ,
      "inputs": [
        "Answer the question based only on the context below.\
         Context: " + format_string(context) + \
         "Question: " + question
      ],
      "parameters": {
        "decoding_method": "greedy",
        "min_new_tokens": 20,
        "max_new_tokens": 200,
        "beam_width": 1
      }
    }

    response = requests.post(model_url, headers=headers, json=json_data)
    json_response = json.loads(response.content.decode("utf-8"))
    return json_response['results'][0]['generated_text']
            
res = process_watsonx_request()
print(res)
with open(cfg['resPath'], "wb") as fp:
    pickle.dump(res,fp)