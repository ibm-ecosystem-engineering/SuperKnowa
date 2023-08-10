# SuperKnowa Backend Service

In this subdirectory houses code, deployment and integration instructions for the SuperKnowa Backend Service.

The SuperKnowa Backend Service is intended to be used in the context of Retrieval Augmented Generation (RAG) application. It leverages an external Information Retrieval service (Solr, Elasticsearch, or Watson Discovery) and a LLM hosted on watsonx.ai in order to answer 
questions about a corpus of data. 

The service exposes an API intended to be called by a front-end application (e.g. a web or mobile app). In addition, it is integrated with MongoDB in order to store questions from users together with answers, as well as user feedback.

## Reference Architecture

![superknowa](https://github.com/EnterpriseLLM/SuperKnowa/assets/111310676/278bced3-9253-4cf7-9b2f-0690b72a9f0b)



## Prerequisites

## Core Service API

## 

## Components

Below are the components that built the superknowa application.

- Superknowa client app
- Superknowa backend server
- Reranker server
- Watsonx.ai
- Retrievers
  - Solr
  - Elasticsearch
  - IBM Watson Discovery
 
## Deployment

- [Run the Backend sever](Backend/)
- [OCP Deployment](Deployment/)
