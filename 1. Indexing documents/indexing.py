## Elastic search indexing
import os
import re
from datetime import date
import pandas as pd
import json
from datetime import datetime
import requests
import PyPDF2

from pathlib import Path
from dateutil.parser import parse

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import yaml



#Reading the content of config file
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    cfg = cfg['indexing']

def pre_processingtext(text_data):
    replaced = re.sub("</?p[^>]*>", "", text_data)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("id=*>;", "", replaced)
    return replaced

def create_elastic_instance(elasticURL,elasticCertPath):
    # create an instance of Elasticsearch with TLS options
    es_client = Elasticsearch(
        elasticURL,
        ca_certs=elasticCertPath
    )
    info = es_client.info()
    print(info)
    return es_client
    

def create_index(indexName,indexMapping,es_client):
    #test the connection and create an index
    try:
        es_client.indices.create(index=indexName,body = indexMapping)
        print(f"Index '{indexName}' created successfully.")
    except RequestError as e:
        if e.error == 'resource_already_exists_exception':
            print(f"Index '{indexName}' already exists.")
        else:
            print(f"An error occurred while creating index '{indexName}': {e}")

## get all files from folder
def get_all_files(folder_name):
    # Change the directory
    os.chdir(folder_name)
    # iterate through all file
    file_path_list =[]
    for file in os.listdir():
        if ".txt" in file:
            file_path = f"{folder_name}/{file}"
            file_path_list.append(file_path)
    return file_path_list


## Assuming files are in text format and cleaned
def indexing_documnet(indexName,file_path,es_client):
     today = date.today()
     with open(file_path, 'r', encoding="latin1") as file:
        if ".txt" in file_path:
            content = file.read()
            print(len(content), file_path)
            if "content:" in content:
                content_value = content.split("content:")
                content = pre_processingtext(content_value[1])
                categories_val = content_value[0].split("categories:")
                categories = categories_val[1]
                sub_title =  categories_val[0].split("sub_title:")
                title_val =  sub_title[0].split("title:")
                title = title_val[1]
                pd_val =  title_val[0].split("publish_date:")
                publish_date = pd_val[1]
                ld_val =  pd_val[0].split("updated_date:")
                updated_date = ld_val[1]
                print("values ---",len(ld_val))
                urls =  ld_val[0].split("URL:")
                print(len(urls))
            
                url = "https://developer.ibm.com/blogs/"+urls[1]

                indexing_date = today
                source = "IBM Developer"
                data = "{'id' : '"+str(title)+"', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'}"
            
                publish_date = publish_date.replace("\n","").strip()
                updated_date = updated_date.replace("\n","").strip()
                print(publish_date)
                print("update_date ",updated_date)
                publish_date_obj = datetime.strptime(publish_date,"%Y-%m-%dT%H:%M:%S")
                publish_date = publish_date_obj.date()

                updated_date_obj = datetime.strptime(updated_date,"%Y-%m-%dT%H:%M:%S")
                updated_date = updated_date_obj.date()
            else:
                content = pre_processingtext(content)
                categories = ""
                sub_title =  ""
                title = ""
                publish_date = today
                updated_date = today
                indexing_date = today
                url =""

            document ={
            "id": ""+title+"",
            "published_source": ""+source+"",
            "publish_date": ""+str(publish_date)+"",
            "last_update_date": ""+str(updated_date)+"",
            "indexing_date": ""+str(indexing_date)+"",
            "content": ""+content+"",
            "url": ""+url+"",
            "keywords": ""+str(sub_title)+"",
            "categories": ""+str(categories)+"",
        }
        response = es_client.index(index=indexName, body=document)
        print(response)
    

indexName = cfg['indexName']
es_client = create_elastic_instance(cfg['elasticURL'],cfg['elasticCertPath'])
create_index(indexName,cfg['indexMapping'],es_client)
file_list = get_all_files(cfg['indexFileFolderPath'])
for file in file_list:
    indexing_documnet(indexName,file,es_client)


    
