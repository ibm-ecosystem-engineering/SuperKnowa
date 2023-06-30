import pysolr
import os
import tika
tika.initVM()
from tika import parser  
import re
from datetime import date
import pandas as pd
import json
from datetime import datetime

today = date.today()
print("Today's date:", today)

def pre_processingtext(text_data):
    replaced = re.sub("</?p[^>]*>", "", text_data)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("id=*>;", "", replaced)
    return replaced

def index_ibm_developerdata():
    with open(file_path, 'r', encoding="latin1") as file:
        if ".txt" in file_path:
            content = file.read()
            print(len(content), file_path)
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
            url = "https://developer.ibm.com/middleware/v1/contents"+urls[1]
            indexing_date = today
            source = "IBM Developer"
            data = "{'id' : '"+str(title)+"', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'}"
            #df = pd.DataFrame({'id' : '""+str(title)+""', 'published_source' : '"+source+"', 'publish_date' : '"+str(publish_date)+"','last_update_date' : '"+str(updated_date)+"','indexing_data' : '"+str(indexing_date)+"', 'url' : '"+url+"','content' : '"+str(content)+"','keywords' : '"+str(sub_title)+"','categories' : '"+str(categories)+"'},index=[i])
            #print(df.to_json(orient="split"))
            
            #json_object = json.loads(data)
            publish_date = publish_date.replace("\n","").strip()
            updated_date = updated_date.replace("\n","").strip()
            print(publish_date)
            print("update_date ",updated_date)
            publish_date_obj = datetime.strptime(publish_date,"%Y-%m-%dT%H:%M:%S")
            publish_date = publish_date_obj.date()

            updated_date_obj = datetime.strptime(updated_date,"%Y-%m-%dT%H:%M:%S")
            updated_date = updated_date_obj.date()

        
            solrdocs.append({
            "id": ""+title+"",
            "published_source": ""+source+"",
            "publish_date": ""+str(publish_date)+"",
            "last_update_date": ""+str(updated_date)+"",
            "indexing_date": ""+str(indexing_date)+"",
            "content": ""+content+"",
            "url": ""+url+"",
            "keywords": ""+str(sub_title)+"",
            "categories": ""+str(categories)+"",
        })
        



  

# Connect to Solr
solr = pysolr.Solr('http://150.239.171.68:8983/solr/combined_metadata/', always_commit=True)

# Directory containing the documents
ibm_docs_dir = '/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/ibm_developer_metadata/'
white_paper_docs_dir ='/Users/abhilashamangal/Documents/GitHub/Foundation-models_main/Scraper/scrape_data/white_paper_metadata/data-2/'

# Iterate over the files in the directory
solrdocs =[]
i =0
for filename in os.listdir(white_paper_docs_dir):
    print("processing i---",i)
    file_path = os.path.join(white_paper_docs_dir, filename)
    
    # Read the contents of the file
    with open(file_path, 'r', encoding="latin1") as file:
        if ".json" in file_path:
            content = file.read()
            json_object = json.loads(content)
            print(json_object)
            source ="IBM White Paper"
            publish_date = json_object['publish_date']
            updated_date = publish_date
            indexing_date = today
            url = json_object['url']
            attachment = json_object['attachment']
            if len(attachment) >1:
                for att in attachment:
                    print(att)

            
                


            solrdocs.append({
            "id": ""+json_object['title']+"",
            "published_source": ""+source+"",
            "publish_date": ""+str(publish_date)+"",
            "last_update_date": ""+str(updated_date)+"",
            "indexing_date": ""+str(indexing_date)+"",
            "content": ""+content+"",
            "url": ""+url+"",
            "keywords": ""+str(sub_title)+"",
            "categories": ""+str(categories)+"",
        })
            
        

            i=i+1
        


#print(solrdocs)
#df = pd.DataFrame(solrdocs)
#data_json = df.to_json()
#solrdocs_new =[]
#solrdocs_new.append(data_json)
#print(df.to_json())
#solr.add(solrdocs)
print("indexed data scussefully")


