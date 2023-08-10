# SuperKnowa Backend Service

This subdirectory contains code, and deployment and integration guides, for the SuperKnowa Backend service.

The SuperKnowa Backend service is intended to be used in the context of Retrieval Augmented Generation (RAG) application. It leverages an external Information Retrieval service (Solr, Elasticsearch, or Watson Discovery) and a LLM hosted on watsonx.ai, in order to answer 
questions about a corpus of data. 

The service exposes an API that is intended to be called by a front-end application (e.g. a web or mobile app). In addition, it is integrated with MongoDB in order to store questions from users together with answers, as well as user feedback.

Note that we do not include a reference front-end application in this directory.

## Reference Architecture

![superknowa](https://github.com/EnterpriseLLM/SuperKnowa/assets/111310676/278bced3-9253-4cf7-9b2f-0690b72a9f0b)

The basic flow is:

1. A user submits a question in natural language to a front-end application.
2. The front-end application forwards the request to the SuperKnowa Backend.
3. The SuperKnowa Backend requests documents from an Information Retrieval service.
4. The SuperKnowa Backend sends the returned documents to a Reranker service.
5. The Reranker sends back the most relevant documents to the SuperKnowa Backend.
6. The SuperKnowa Backend creates a prompt for the LLM running on watsonx.ai, which consists of a context generated from the most relevant documents as well as the user's original question.
7. The LLM returns a generated answer to the SuperKnowa Backend.
8. The SuperKnowa Backend passes the message to the front-end application.
9. The front-end application sends the message to the user.

## Prerequisites

The SuperKnowa Backend relies on the following external services which must be deployed in advance.

- You have deployed the Reranker service.
- You have deployed a LLM with watsonx.ai.
- You have indexed a corpus of data with one of the following Information Retrievers:
  - Solr
  - Elasticsearch
  - IBM Watson Discovery
- You have deployed MongoDB. You can use the IBM Cloud MongoDB service for example.
- (Optional) For OpenShift deployment, you will need an OpenShift cluster on which you can deploy applications.

## Deploy the Backend Service

- [Deploy locally](Backend/)
- [Deploy on OpenShift](Deployment/)

## Test the API
