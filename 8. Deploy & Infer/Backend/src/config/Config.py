import os
import requests
import json

class Config:

    MODEL_SERVICE_URL =  os.getenv('MODEL_SERVICE_URL')
    MODEL_AUTH_TOKEN = os.getenv('MODEL_AUTH_TOKEN')
    url = os.getenv('WD_URL')

    # Watson discovery information
    WD_AUTH_KEY = os.getenv('WD_AUTH_KEY')
    project_id = os.getenv('WD_PROJECT_ID')
    collection_id = os.getenv('WD_COLLECTION_ID')
    max_num_documents=10

    # Solr backend information
    SOLR_BACKEND = os.getenv('SOLR_BACKEND')

    # Reranking backend
    RERANKER_URL = os.getenv('RERANKER_URL')

    # MongoDB backend
    MONGO_URL=os.getenv('MONGO_URL')
    MONGO_DB=os.getenv('MONGO_DB')
    MONGO_USER=os.getenv('MONGO_USER')
    mongo_pass=os.getenv('MONGO_PASS')

    # Elastic Server 
    elasticUrl = os.getenv("ELASTIC_URL")

    # Retriever URL
    RETRIEVER = os.getenv("CONTEXT_RETRIEVER", default="solr")    

    def __init__(self) -> None:
        pass

    def format_model_output(self, model_output):
        # formatting BAM Model output
        model_output = model_output.replace("Question", '')
        model_output = model_output.replace("Answer: ", '')
        model_output = model_output.replace("Context: ", '')
        model_output = model_output.replace("answer: ", '')
        model_output = model_output.strip()
        # Seprate sentences
        sentences = model_output.split(". ")
        # remove duplicates SENTENCES
        unique_sentences = list( dict.fromkeys(sentences))

        if(len(unique_sentences) == 1):
            return unique_sentences[0].strip().capitalize() + "."

        if not model_output.endswith("."):
        # remove the last sentence if not . at last
            unique_sentences.pop()

        # join unique sentences back into a text 
        model_output = ". ".join(unique_sentences)+ "."
        return model_output
    
    def get_model_id(self,info_collect):
        model_id = ""
        if("info" in info_collect):
            info = info_collect["info"]
            if("success" in info):
                model_id = info["success"]["model_name"]

        return model_id
    
    def reranking(self,question, max_reranked_documents, results_list):
        
        if len(results_list) >0:
            response = requests.post(
                Config.RERANKER_URL, 
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