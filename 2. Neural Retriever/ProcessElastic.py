import pickle
import os
import numpy as np
import pandas as pd
#from src.config.Config import Config
import datetime
import time
import requests
import re
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import yaml

#Reading the content of config file
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    cfg = cfg['retriever']



def skip_unwanted_characters(document, keyword):
    lines = document.split('\n')
    desired_text = ""
    last_occurrence = -1
    for i, line in enumerate(lines):
        if keyword in line:
            last_occurrence = i
            
    if last_occurrence != -1:
        for line in lines[last_occurrence+1:]:
            desired_text += line.strip() + "\n"
    else:
        desired_text = document

    return desired_text.strip()

def pre_processingtext(text_data):
    replaced = re.sub("\{{ .*?\}}", "", text_data)
    replaced = re.sub("\{: .*?\}", "", text_data)
    replaced = re.sub("\(.*?\)|\[.*?\] |\{.*?\}", "", replaced)
    replaced = re.sub("</?div[^>]*>", "", replaced)
    replaced = re.sub("</?p[^>]*>", "", replaced)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("</?href*>", "", replaced)
    replaced = replaced.replace("}","")
    replaced = replaced.replace("##","")
    replaced = replaced.replace("###","")
    replaced = replaced.replace("#","")
    replaced = replaced.replace("*","")
    replaced = replaced.replace("<strong>","")
    replaced = replaced.replace("</strong>","")
    replaced = replaced.replace("<ul>","")
    replaced = replaced.replace("</ul>","")
    replaced = replaced.replace("<li>","")
    replaced = replaced.replace("</li>","")
    replaced = replaced.replace("<ol>","")
    replaced = replaced.replace("</ol>","")
    return replaced


def elastic_retervier(indexName,question):
    results_list=[]
    # Create an instance of Elasticsearch with TLS options
    es_client = Elasticsearch(cfg['elasticURL'],ca_certs="5cb6eb86-ae1c-11e9-99c9-6a007ab2fc0b")
    info = es_client.info()
    print(info)
    index_name = indexName
    search_query5 ={
    "query": {
        "bool": {
        "must": [
        { "match": { "content": f"'{question}'" }}
    ],
        "must_not": [
        { "match": { "published_source": "Redbooks" }}
    ]
        }
    }
    }
    ## Top 10 documents 
    response = es_client.search(
    index=index_name,
    body=search_query5,
    scroll='5m',  # Set the scroll timeout (e.g., 5 minutes)
    size=10  # Set the number of documents to retrieve per scroll
    )
    all_hits = response['hits']['hits']
    i =0
    print(len(all_hits))
    for num, doc in enumerate(all_hits):
        doc_id = doc["_source"]["id"]
        doc_url = doc["_source"]["url"].replace(" ","")
        doc_source = doc["_source"]["published_source"]
        string_unicode = doc["_source"]["content"]
        doc = string_unicode.encode("ascii", "ignore")
        string_decode = doc.decode()
        keyword = "{: shortdesc} "
        cleaned_text = skip_unwanted_characters(string_decode,keyword)
        pattern =  r'\{\s*:\s*[\w#-]+\s*\}|\{\s*:\s*\w+\s*\}|\n\s*\n'
        cleaned_text = re.sub(pattern, '', cleaned_text)
        cleaned_text = pre_processingtext(cleaned_text)
        query_hits = {
                    "document": {
                        "rank": i,
                        "document_id": doc_id,
                        "text": cleaned_text[0:4000], 
                        "url" : doc_url,
                        "source":doc_source
                    },
                }

        results_list.append(query_hits)
        results_to_display = [results_list['document'] for results_list in results_list]
        df = pd.DataFrame.from_records(results_to_display, columns=['rank','document_id','text','url','source'])
        # df['title'] = np.random.randint(1, 10, df.shape[0])
        df.dropna(inplace=True)
        i = i+1
    return results_list

print(cfg)
res = elastic_retervier(cfg['indexName'],cfg['query'])

with open(cfg['resPath'], "wb") as fp:
    pickle.dump(res,fp)
print(res)
