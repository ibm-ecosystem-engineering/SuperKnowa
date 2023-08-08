# Superknowa backend server

To run the server locally please follow the below steps.

## Prerequisites

- A MongoDB server
- Reranker service ( we are using DrDecr model from primeQA)
- Retriever ( Elasticsearch)
- [Python 3.9](https://www.python.org/downloads/) or later

## Create environment

```sh
python3 -m venv backend
```

```sh
source backend/bin/activate
```

## Install requirement

```sh
pip3 install -r requirement.txt
```
## Model configurations

We are storing the watsonx model configuration in mongodb collection name 'model_config', please store the below configuration in 'model_config' collection, you can add modify based on your requirements.

```json
{
  "models": [
    {
      "model_id": "google/ul2",
      "prompt": "Answer the question based on the context below.",
      "inputs": [],
      "parameters": {
        "temperature": 0.3,
        "min_new_tokens": 10,
        "max_new_tokens": 200
      }
    },
    {
      "model_id": "google/flan-ul2",
      "prompt": "Answer the question based on the context below.",
      "inputs": [],
      "parameters": {
        "temperature": 0.3,
        "min_new_tokens": 10,
        "max_new_tokens": 150
      }
    },
    {
      "model_id": "google/flan-t5-xxl",
      "inputs": [],
      "prompt": "Answer the question based on the context below.",
      "parameters": {
        "temperature": 0.3,
        "min_new_tokens": 10,
        "max_new_tokens": 150
      }
    },
    {
      "model_id": "tiiuae/falcon-40b",
      "prompt": "Answer the question based on the context below.",
      "inputs": [],
      "parameters": {
        "temperature": 0.3,
        "min_new_tokens": 10,
        "max_new_tokens": 150
      }
    },
    {
      "model_id": "google/flan-t5-xl",
      "prompt": "Answer the question based on the context below.",
      "inputs": [],
      "parameters": {
        "temperature": 0.3,
        "min_new_tokens": 10,
        "max_new_tokens": 150
      }
    }
  ]
}
```

## Setup environment variables

```sh
export MODEL_SERVICE_URL=<Watsonx.ai workbench api url>
export MODEL_AUTH_TOKEN='Bearer <Auth token>'
export WD_URL=<Watson Discovery URL>
export WD_AUTH_KEY=<Watson Discovery authentication key>
export WD_PROJECT_ID='<Watson Discovery project id>'
export WD_COLLECTION_ID='<Watson Discovery collection id>'
export SOLR_BACKEND=<Solr server url>
export RERANKER_URL=<Rerank server url>
export MONGO_URL='<MONGODB Server url>'
export MONGO_DB=<MongoDB Database name>
export MONGO_PASS='<MongoDB password>'
export MONGO_USER='<MongoDB user>'
export ELASTIC_URL='<Elasticsearch url with user and password>'
```

## Run the server

```
python3 main.py
```
## TEST

### Multi model call

```sh
curl --location 'http://localhost:3001/api/v1/chat/multi/elastic/3' \
--header 'Content-Type: application/json' \
--data '{
    "question":"what is turbonomic?"
}'
```

### Single model call

```sh
curl --location 'http://localhost:3001/api/v1/chat/elastic' \
--header 'Content-Type: application/json' \
--data '{
    "question":"what is sap btp?"
}'
```

