import json
import re
import requests
from bs4 import BeautifulSoup
import os

from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

dwKey = os.getenv('WD_KEY')
wdURL = os.getenv('WD_URL')
wdProjectId = os.getenv('WD_PROJECT_ID')
wdCollectionId = os.getenv('WD_COLLECTION_ID')

def process_discovery_retriever(question):
    # Inner Structure - User Input
    question_answer_dict = {"question" : question}

    # Discovery Setup
    url = wdURL
    project_name = 'kobayashi-maru-III'
    collection_name = 'SuperKnowa'
    project_id = wdProjectId
    collection_id = wdCollectionId

    # Discovery Service Handling
    authenticator = IAMAuthenticator(dwKey)
    discovery = DiscoveryV2(
        version='2020-08-30',
        authenticator=authenticator
    )

    # Project Handling
    projects = discovery.list_projects().get_result()
    for project in projects['projects']:
        if (project['name'] == project_name):
            project_id = project['project_id']

    # Collection Handling
    collections = discovery.list_collections(project_id = project_id).get_result()
    for collection in collections['collections']:
        # print(collection)
        if (collection['name'] == collection_name):
            collection_id = collection['collection_id']

    def format_string(str):
        string_encode = string_unicode.encode("ascii", "ignore")
        string_decode = string_encode.decode()
        cleantext = BeautifulSoup(string_decode, "lxml").text
        perfecttext = " ".join(cleantext.split())
        perfecttext = re.sub(' +', ' ', perfecttext).strip('"')
        return perfecttext

    discovery.set_service_url(url)

    # Processing Setup
    query_text = question_answer_dict['question']
    query_result = discovery.query(project_id=project_id, query=query_text).get_result() # Only Discovery's first/best match will be considered.
    string_unicode = query_result['results'][0]['document_passages'][0]['passage_text']  # Get the passage from the document
    query_result_text = format_string(string_unicode)  # Get rid of unicode and HTML tags - The passage text
    # print("Passage: ",query_result_text)
    return query_result_text

def main():
    question = "What is Cloud Pak for data?"
    answer = process_discovery_retriever(question)
    print("FINAL ANSWER: ", answer)
    return answer

if __name__ == "__main__":
    main()