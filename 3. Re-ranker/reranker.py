import time,json
import pandas as pd
import yaml
import pickle,requests

#Reading the content of config file
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    cfg = cfg['reranker']

reranker_url = cfg['reranker_url']
max_reranked_documents = cfg['max_reranked_documents']
question = cfg['query']
with open (cfg['listOfDocuments'], 'rb') as fp:
    results_list = pickle.load(fp)


def reranking(question, max_reranked_documents, results_list):
    
    if len(results_list) >0:
        response = requests.post(
            reranker_url, 
            headers={'Content-Type': 'application/json'}, 
            data= json.dumps({
                "question": question,
                "documents": results_list,
                "max_num_documents": max_reranked_documents
            }),verify=False)

        if(response.status_code == 200):
            json_response = json.loads(response.text)
            return json_response["context"], json_response["source_url"]
        else:
            print("status code,", response.status_code)
            return "None" , "None"           
    else:
        return "None" , "None"

context, source_url =  reranking(question,max_reranked_documents,results_list)

with open(cfg['resPath'], "wb") as fp:
    pickle.dump(context,fp)

print(context)
print(source_url)
