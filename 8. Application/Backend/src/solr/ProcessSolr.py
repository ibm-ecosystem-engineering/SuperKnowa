import os
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import numpy as np
import pandas as pd
from src.config.Config import Config
import datetime
import time
import requests
import re
import urllib.parse
import json

class ProcessSolr:
    
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
    
    # Superknow version of the retriver
    def solr_reteriver(self, question, info_collect):
        # replace question mark from question
        question = question.replace('?', '').strip()
        print("processing....", question)
        # url encoding the query
        question_encode = urllib.parse.quote(question)
        # Prepare solr query
        # http://150.239.171.68:8983/solr/superknowa/select?q=*:*&q.op=AND&wt=json&fq=!published_source:Redbooks
        solr_requst_url = f'{Config.SOLR_BACKEND}?q={question_encode}&q.op=AND&wt=json&fq=!published_source:Redbooks'
        info_collect["solr_request"] = solr_requst_url
        print(solr_requst_url)
        # Make solr requests
        response = requests.get(solr_requst_url)
        query_result = response.json()
        
        # print("SOLR RESPONSE:", json.dumps(query_result, indent=2))
        print(query_result['response']['numFound'], "documents found.")
        total = query_result['response']['numFound']
        results_list=[]
        query_hits={}
        if total > 0:
            if total > 10:
                total =10
            for i in range(total):
                    string_unicode = " ".join(query_result['response']['docs'][i]['content'])
                    doc = string_unicode.encode("ascii", "ignore")
                    string_decode = doc.decode()
                    keyword = "{: shortdesc} "
                    cleaned_text = self.skip_unwanted_characters(string_decode, keyword)
                    pattern =  r'\{\s*:\s*[\w#-]+\s*\}|\{\s*:\s*\w+\s*\}|\n\s*\n'
                    cleaned_text = re.sub(pattern, '', cleaned_text)
                    cleaned_text = self.pre_processingtext(cleaned_text)
                    query_hits = {
                    "document": {   
                        "rank": i,
                        "document_id": query_result['response']['docs'][i]['id'][0],
                        "text": cleaned_text[0:4000], 
                        "url" :query_result['response']['docs'][i]['url'][0].replace(" ","")
                        },
                    }

                    results_list.append(query_hits)
                    results_to_display = [results_list['document'] for results_list in results_list]
                    df = pd.DataFrame.from_records(results_to_display, columns=['rank','document_id','text','url'])
                    # df['title'] = np.random.randint(1, 10, df.shape[0])
                    df.dropna(inplace=True)
                    #print('======================================================================')             
        return results_list
