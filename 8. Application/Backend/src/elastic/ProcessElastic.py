import os
import numpy as np
import pandas as pd
from src.config.Config import Config
import datetime
import time
import requests
import re
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

class ProcessElastic:
    
    def __init__(self) -> None:
        pass

    def skip_unwanted_characters(self, document, keyword):
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
    
    def pre_processingtext(self,text_data):
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

 
    def elastic_retervier(self,question):
        results_list=[]
        # Create an instance of Elasticsearch with TLS options
        es_client = Elasticsearch(Config.elasticUrl,ca_certs="cert/elastic.crt")
        info = es_client.info()
        print(info)
        index_name = 'superknowa'
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
            cleaned_text = self.skip_unwanted_characters(string_decode,keyword)
            pattern =  r'\{\s*:\s*[\w#-]+\s*\}|\{\s*:\s*\w+\s*\}|\n\s*\n'
            cleaned_text = re.sub(pattern, '', cleaned_text)
            cleaned_text = self.pre_processingtext(cleaned_text)
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
