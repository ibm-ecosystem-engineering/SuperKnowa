import json
import re
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
from IPython.display import display, HTML

# Run ColBERT Reranker
from primeqa.components.reranker.colbert_reranker import ColBERTReranker
model_name_or_path = "DrDecr.dnn"


llmToken = os.getenv('LLM_TOKEN')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


# Retrieve documents
max_num_documents=10
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
    question = question.replace("?","")
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

   

def solr_reranker(question, max_reranked_documents = 10):

    reranker = ColBERTReranker(model=model_name_or_path)
    reranker.load()
    
    results_list = solr_reteriver(question)
    if len(results_list) >0:
        reranked_results = reranker.predict(queries= [question], documents = [results_list], max_num_documents=max_reranked_documents)

        print(reranked_results)

        reranked_results_to_display = [result['document'] for result in reranked_results[0]]
        df = pd.DataFrame.from_records(reranked_results_to_display, columns=['rank','document_id','text','url'])
        print('======================================================================')
        print(f'QUERY: {question}')
        display( HTML(df.to_html()) )
        return df['text'][0] , df['url'][0]
    else:
        return "0 documents found" , "None"

def format_string(doc):
    doc = doc.encode("ascii", "ignore")
    string_decode = doc.decode()
    cleantext = BeautifulSoup(string_decode, "lxml").text
    perfecttext = " ".join(cleantext.split())
    perfecttext = re.sub(' +', ' ', perfecttext).strip('"')
#     perfecttext = perfecttext[0:4000]
    return perfecttext

def process_llm_request(question):
    
    wd_result,url = solr_reranker(question)
    if '0 documents found' not in wd_result:
        combined_input = "Answer the question based only on the context below. " + \
            "Context: "  + format_string(wd_result) + \
            " Question: " + question
        print("INPUT PROMPT: ", combined_input)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': llmToken,
        }

        json_data = {
            'model_id': 'bigscience/bloom',
            # 'inputs': [
            #     messageText,
            # ],
            'inputs':  [combined_input],
            # "inputs": ["Answer the question based only on the context below. \
            #     Context: IBM Cloud Pak for Data offers the IBM Watson Knowledge Catalog service, which provides a number of features to incorporate such policy security, and compliance features and to govern your data. A data steward or administrator can use the IBM Watson Knowledge Catalog to build a governance catalog consisting of terms policies, and rules that can help govern and secure the data. \
            #     Question: What is Watson Knowledge catalog?"],        
                'parameters': {
                # "stream": "true",
                'temperature': 0.5,
                'max_new_tokens': 200,
            },
        }

        ## demo link of llm server will be replace with original link
        response = requests.post('https://llm-api.res.ibm.com/v1/generate', headers=headers, json=json_data)
        json_response = json.loads(response.content.decode("utf-8"))
        result = json_response['results'][0]['generated_text'].split("Answer:")
        if len(result) > 1:
            print("LLM Output: ", result[1])
            return result[1],url
        else:
            print("LLM Output: ", result[0])
            return result[0],url
    else:
        return "0 documents found" , "None"

def main():
    question = "what is ibm cloud pak for data"
    # print("-------- Final answer ---------------")
    answer ,url = process_llm_request(question)
    print("FINAL ANSWER: ", answer)
    print("URL: ", url)
    return answer , url

if __name__ == "__main__":
    main()
