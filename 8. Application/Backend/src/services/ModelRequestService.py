from bs4 import BeautifulSoup
import re
from src.discovery.ProcessDiscovery import ProcessDiscovery
import requests
import json
import os
from src.config.Config import Config
import time
from src.solr.ProcessSolr import ProcessSolr
from src.services.ModelConfig import ModelConfig
from src.elastic.ProcessElastic import ProcessElastic
from src.services.RetrieverService import RetrieverService
import pandas as pd

class ModelRequestService:

    def __init__(self, model_configurations):
        self.modelConfig = ModelConfig(model_configurations)

    def format_string(self, doc):
        doc = doc.encode("ascii", "ignore")
        string_decode = doc.decode()
        cleantext = BeautifulSoup(string_decode, "lxml").text
        perfecttext = " ".join(cleantext.split())
        perfecttext = re.sub(' +', ' ', perfecttext).strip('"')
    #   perfecttext = perfecttext[0:4000]
        return perfecttext
    #
    # The source documents are watson discovery, first it calls wd and rerank
    #
    def process_request_using_wd(self, question, authenticator, info_collect):
        
        info = {}
        info_collect['info'] = info

        tic = time.perf_counter()
        wdiscovery = ProcessDiscovery(authenticator)
        toc = time.perf_counter()
        duration = toc - tic
        info['discovery_load_time'] = duration
        print(f"Watson discovery authentication loading ==> {toc - tic:0.4f} seconds")
    
        tic = time.perf_counter()
        wd_result = wdiscovery.WD_reranker(question=question, max_reranked_documents=4)
        toc = time.perf_counter()
        duration = toc - tic
        info['reranker_load_time'] = duration
        print(f"Watson discovery reranking ==> {toc - tic:0.4f} seconds")

        context = self.format_string(wd_result)

        if(context == "None"):
            return "None"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': Config.MODEL_AUTH_TOKEN,
        }
        
        fail_info_list = []

        for model in self.modelConfig.models(question, context):
            
            # get the promot for logging..
            prompt = model["prompt"]
            # delete prompt key from object
            del model["prompt"]

            tic = time.perf_counter()
            response = requests.post(Config.MODEL_SERVICE_URL, headers=headers, json=model)
            toc = time.perf_counter()
            duration = toc - tic
            print(f"model '{model['model_id']}' loading time ==> {toc - tic:0.4f} seconds")

            if(response.status_code == 200):
                model_info = {}
                model_info['model_name'] = model['model_id']
                model_info['model_load_time'] = duration
                model_info['prompt'] = prompt
                info['success'] = model_info
                json_response = json.loads(response.content.decode("utf-8"))
                return json_response['results'][0]['generated_text']
            else:
                print(f"model {model['model_id']} -> {response.status_code} -> {response}")
                fail_info = {}
                fail_info['model_name'] = model['model_id']
                fail_info['model_load_time'] =duration
                fail_info['prompt'] = prompt
                fail_info['error_msg'] = f"Request failed with status code: {response.status_code}"
                fail_info_list.append(fail_info)
                info['failed_model'] = fail_info_list
                
            
        return "No document found for this question"
    
    #
    # The source documents are from solr query, first it calls solr and then rerank
    #
    def process_request_using_single_model(self, question, retriever, info_collect):
        info = {}
        info_collect['info'] = info

        config = Config()
        retriver_svc = RetrieverService()
        context, source_url = retriver_svc.retrieve_documents(info=info, question=question, retriever=retriever)

        if(context == "None"):
            return "None", source_url

        headers = {
            'Content-Type': 'application/json',
            'Authorization': Config.MODEL_AUTH_TOKEN,
        }
        
        fail_info_list = []

        for model in self.modelConfig.models(question, context):
            # get the promot for logging..
            prompt = model["prompt"]
            # delete prompt key from object
            del model["prompt"]
            tic = time.perf_counter()
            response = requests.post(Config.MODEL_SERVICE_URL, headers=headers, json=model)
            toc = time.perf_counter()
            duration = toc - tic
            print(f"model '{model['model_id']}' loading time ==> {toc - tic:0.4f} seconds")

            if(response.status_code == 200):
                model_info = {}
                model_info['model_name'] = model['model_id']
                model_info['model_load_time'] =duration
                model_info['prompt'] = prompt
                info['success'] = model_info
                json_response = json.loads(response.content.decode("utf-8"))
                return json_response['results'][0]['generated_text'], source_url
            else:
                print(f"model {model['model_id']} -> {response.status_code} -> {response}")
                fail_info = {}
                fail_info['model_name'] = model['model_id']
                fail_info['model_load_time'] = duration
                fail_info['prompt'] = prompt
                fail_info['error_msg'] = f"Request failed with status code: {response.status_code}, Reason: {str(response.reason)}"
                fail_info_list.append(fail_info)
                info['failed_model'] = fail_info_list
            
        return "No document found for this question", source_url
    
#
    # The source documents are from solr query, multi model, first it calls solr and then rerank
    #
    def process_request_multi_model(self, question, retriever, info_collect, number_of_model=3):
        info = {}
        info_collect['info'] = info

        config = Config()
        retriver_svc = RetrieverService()
        context, source_url = retriver_svc.retrieve_documents(info=info, question=question, retriever=retriever)

        results = []

        if(context == "None"):
            for i in range(int(number_of_model)):
                non_res = {}
                non_res["answer"] = "No document found for this question."
                non_res["source"] = ""
                non_res["question"] = question
                non_res["model_id"] = ""
                non_res['model_load_time']= ""
                results.append(non_res)
            info_collect["results"] = results
            return "None", source_url

        headers = {
            'Content-Type': 'application/json',
            'Authorization': Config.MODEL_AUTH_TOKEN,
        }
        
        fail_info_list = []

        count = int(number_of_model)

        for model in self.modelConfig.models(question, context):
            
            if(count <= 0 ):
                break

            result = {}

            # get the promot for logging..
            prompt = model["prompt"]
            # delete prompt key from object
            del model["prompt"]

            tic = time.perf_counter()
        
            response = requests.post(Config.MODEL_SERVICE_URL, headers=headers, json=model)
            toc = time.perf_counter()
            duration = toc - tic
            print(f"model '{model['model_id']}' loading time ==> {toc - tic:0.4f} seconds")

            if(response.status_code == 200):
                json_response = json.loads(response.content.decode("utf-8"))
                
                answer = json_response['results'][0]['generated_text']
                afterFormat = config.format_model_output(answer)
                result['prompt'] = prompt
                result["raw_answer"] = answer
                result["answer"] = afterFormat
                result["source"] = source_url
                result["question"] = question
                result["model_id"] = model['model_id']
                result['model_load_time'] =duration
                results.append(result)

                count = count - 1
            else:
                print(f"model {model['model_id']} -> {response.status_code} -> {response}")
                fail_info = {}
                fail_info['prompt'] = prompt
                fail_info['model_name'] = model['model_id']
                fail_info['model_load_time'] =duration
                fail_info['error_msg'] = f"Request failed with status code: {response.status_code}, Reason: {str(response.reason)}"
                fail_info_list.append(fail_info)
            
            info['failed_model'] = fail_info_list
            info_collect["results"] = results
                
    #
    # This service will process request with given context passed by user. No reranking and document searching.
    #
    def process_request_with_given_context(self, question, context, info_collect):
        info = {}
        info_collect['info'] = info

        context = self.format_string(context)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': Config.MODEL_AUTH_TOKEN,
        }
        
        fail_info_list = []

        for model in self.modelConfig.models(question, context):
            # get the promot for logging..
            prompt = model["prompt"]
            # delete prompt key from object
            del model["prompt"]

            print("======================================")
            print(model, "Model-config")
            print("======================================")
            
            tic = time.perf_counter()
            response = requests.post(Config.MODEL_SERVICE_URL, headers=headers, json=model)
            toc = time.perf_counter()
            duration = toc - tic
            print(f"model '{model['model_id']}' loading time ==> {toc - tic:0.4f} seconds")


            if(response.status_code == 200):
                model_info = {}
                model_info['model_name'] = model['model_id']
                model_info['model_load_time'] =duration
                model_info['prompt'] = prompt
                info['success'] = model_info
                json_response = json.loads(response.content.decode("utf-8"))
                return json_response['results'][0]['generated_text']
            else:
                print(f"model {model['model_id']} -> {response.status_code} -> {response}")
                fail_info = {}
                fail_info['model_name'] = model['model_id']
                fail_info['prompt'] = prompt
                fail_info['model_load_time'] =duration
                fail_info['error_msg'] = f"Request failed with status code: {response.status_code}, Reason: {str(response.reason)}"
                fail_info_list.append(fail_info)
                info['failed_model'] = fail_info_list
            
        return "No document found for this question"
    
                


