## Import libs
import json
import re
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np

# Retrieve documents
max_num_documents=10

## Removibg unwanted text
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

## Removing some HTML tags form content
def pre_processingtext(text_data):
    replaced = re.sub("\{{ .*?\}}", "", text_data)
    replaced = re.sub("\{: .*?\}", "", replaced)
    replaced = re.sub("\.*?", "", replaced)
    replaced = re.sub("\(.*?\)|\[.*?\] |\{.*?\}", "", replaced)
    replaced = re.sub("</?div[^>]*>", "", replaced)
    replaced = re.sub("</?p[^>]*>", "", replaced)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("</?href*>", "", replaced)
    replaced = re.sub("\s+", " ", replaced)
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


# Retrieve documents
max_num_documents=10

def solr_reteriver(question):
    response = requests.get(f'http://150.239.171.68:8983/solr/superknowa/select?q='+question+'&q.op=AND&wt=json')
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
                string_unicode = query_result['response']['docs'][i]['content'][0]
                doc = string_unicode.encode("ascii", "ignore")
                string_decode = doc.decode()
                keyword = "{: shortdesc} "
                cleaned_text = skip_unwanted_characters(string_decode, keyword)
                pattern =  r'\{\s*:\s*[\w#-]+\s*\}|\{\s*:\s*\w+\s*\}|\n\s*\n'
                cleaned_text = re.sub(pattern, '', cleaned_text)
                cleaned_text = pre_processingtext(cleaned_text)
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
                print('======================================================================')             
    print(f'QUERY: {question}')
    return results_list

## format string 
def format_string(doc):
    doc = doc.encode("ascii", "ignore")
    string_decode = doc.decode()
    cleantext = BeautifulSoup(string_decode, "lxml").text
    perfecttext = " ".join(cleantext.split())
    perfecttext = re.sub(' +', ' ', perfecttext).strip('"')
#     perfecttext = perfecttext[0:4000]
    return perfecttext

def main():
    question = "what is ibm cloud pak for data"
    # print("-------- Final answer ---------------")
    answer ,url = solr_reteriver(question)
    print("FINAL ANSWER: ", answer)
    print("URL: ", url)
    return answer , url

if __name__ == "__main__":
    main()