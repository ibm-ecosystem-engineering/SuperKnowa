from flask import Flask, request, jsonify
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from bs4 import BeautifulSoup
import re
import json
import requests
import time
import os
from flask_cors import CORS
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from src.services.ModelRequestService import ModelRequestService
from src.config.Config import Config
from src.mongo.MongoConnect import MongoConnect
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
from src.services.FileContextService import FileContextService

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SUPERKNOWA')

app = Flask(__name__)
CORS(app)

dbc = MongoConnect()
additional_feedback_collection = dbc.get_collection("additional_feedback")
feedback_collection = dbc.get_collection("feedback")
request_history_collection = dbc.get_request_history()
request_history_context_collection = dbc.get_collection("request_history_context")
authenticator = IAMAuthenticator(Config.WD_AUTH_KEY)
model_configurations = dbc.get_models()

@app.route("/")
def home():
    return {"msg": "working"}

# makes call on watson discovery first
@app.route('/api/v1/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data['question']
    #regenerate = data['regenerate']
    info_collect = {}
    model_request = ModelRequestService(model_configurations)
    model_output =  model_request.process_request_using_wd(question, authenticator, info_collect)
    info_collect['raw_answer'] = model_output

    config = Config()
    model_output = config.format_model_output(model_output)
    info_collect['question'] = question
    info_collect['request_time'] = datetime.now()
    info_collect["answer"] = model_output
    info_collect["retiever"] = "wd"
    info_collect["type"] = "single_model"

    insert_id = request_history_collection.insert_one(info_collect)
    response = {
                    'answer': model_output, 
                    'ref': str(insert_id.inserted_id), 
                    "model_id": config.get_model_id(info_collect)
                }
    return json_util.dumps(response)

@app.route('/api/v1/chat/<retriever>', methods=['POST'])
def chat_single_model(retriever):
    data = request.get_json()
    question = data['question']
    info_collect = {}
    #regenerate = data['regenerate']
    
    model_request = ModelRequestService(model_configurations)
    answer, source = model_request.process_request_using_single_model(question,retriever, info_collect)
    info_collect['raw_answer'] = answer

    config = Config()
    if(answer == "None"):
        answer = "No document found for this question"
    else:
        answer = config.format_model_output(answer)

    info_collect['question'] = question
    info_collect['request_time'] = datetime.now()
    info_collect["answer"] = answer
    info_collect["type"] = "single_model"
    info_collect["retiever"] = retriever

    insert_id = request_history_collection.insert_one(info_collect)

    response = {
                    'answer': answer, 
                    'source': source, 
                    'ref': str(insert_id.inserted_id), 
                    "model_id": config.get_model_id(info_collect)
                }
    return json_util.dumps(response)


@app.route('/api/v1/chat/context/upload', methods=['POST'])
def upload_context_file():
    logger.info('file upload starts')
    file = request.files['file'] 
    fileContext = FileContextService()
    text = fileContext.extract_text_from_pdf(file)
    paragraph = fileContext.separate_paragraphs(text)
    logger.info(paragraph)
    return jsonify({'paragraph': paragraph})

@app.route('/api/v1/chat/context', methods=['POST'])
def chat_with_given_context(): 
    data = request.get_json()
    config = Config()
    info_collect = {}
    paragraph = data['paragraph']
    question = data['question']
    fileContext = FileContextService()
    context = fileContext.find_most_similar_text(question, paragraph) 

    model_request = ModelRequestService(model_configurations)
    model_output =  model_request.process_request_with_given_context(question, context=context, info_collect=info_collect)
    config = Config()
    answer = config.format_model_output(model_output)
    info_collect['question'] = question
    info_collect['request_time'] = datetime.now()
    info_collect['raw_answer'] = model_output
    info_collect["answer"] = answer
    
    info_collect["type"] = "custom_context"
    info_collect["retiever"] = "custom_context"

    logger.info(info_collect)
    
    insert_id = request_history_context_collection.insert_one(info_collect)

    response = {
                    'answer': answer, 
                    'source': "", 
                    'ref': str(insert_id.inserted_id), 
                    "model_id": config.get_model_id(info_collect)
                }

    return json_util.dumps(response)


@app.route('/api/v1/chat/multi/<retriever>/<no_model>', methods=['POST'])
def chat_multi_model(retriever, no_model):
    data = request.get_json()
    question = data['question']
    #regenerate = data['regenerate']
    info_collect = {}
    model_request = ModelRequestService(model_configurations)
    model_request.process_request_multi_model(question=question, retriever=retriever, info_collect=info_collect, number_of_model=no_model)
    info_collect['request_time'] = datetime.now()
    info_collect["type"] = "multi_model"
    info_collect["retiever"] = Config.RETRIEVER

    insert_id = request_history_collection.insert_one(info_collect)
    results = []
    if "results" in info_collect:
        results = info_collect["results"]

    response = { 'results': results, 'ref': str(insert_id.inserted_id) }
    return json_util.dumps(response)

@app.route('/api/v1/feedback/add/<mongo_ref>', methods=['PUT'])
def add_feedback(mongo_ref):
    data = request.get_json()
    if(mongo_ref):
        data['l_id'] = ObjectId(mongo_ref)

    insert = feedback_collection.insert_one(data)
    return json_util.dumps({"feedback_ref": str(insert.inserted_id)})


@app.route('/api/v1/feedback/add/multi_additional/<feedback_id>', methods=['POST'])
def add_additional_feedback_feedback(feedback_id):
    data = request.get_json()
    update = feedback_collection.update_one({'_id': ObjectId(feedback_id)}, {'$push': {'additional_feedback': data}})
    return json_util.dumps({"feedback_ref": str(update.upserted_id)})

@app.route('/api/v1/feedback/update/<feedback_id>', methods=['POST'])
def update_feedback(feedback_id):
    #existing = feedback_collection.find_one({'_id': ObjectId(id)})
    #if(existing):
    data = request.get_json()
    update = feedback_collection.update_one({'_id': ObjectId(feedback_id)}, {"$set": data})
    return json_util.dumps({"feedback_ref": str(update.upserted_id)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3001)