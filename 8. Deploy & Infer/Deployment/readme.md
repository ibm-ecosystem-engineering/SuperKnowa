# Deploy RAG Pipeline

## 1. Deploy to OCP

### Prerequisites 
(Change commands to deploy to another cloud)
- A Kubernetes or Red Hat OpenShift cluster on which you can deploy an application
- A MongoDB server
- Reranker service ( we are using DrDecr model from primeQA)
- Retriever ( Elasticsearch or solr or Watson Discovery)
- [Python 3.9](https://www.python.org/downloads/) or later


## 1. Build the docker image

### Clone the github repo

```sh
git clone https://github.com/EnterpriseLLM/SuperKnowa.git
cd 8.\ Application/Backend/
```

```sh
docker build -t <IMGAGE_REGISTRY>/<NAMESPACE>/<IMAGE_NAME>:<IMAGE_TAG>
```

push the image to the image registry

## 2. Prepeare configuration

### Create a secret

```sh
oc create secret generic superknowa-backend-config \
--from-literal MODEL_SERVICE_URL=<Watsonx.ai workbench api url> \
--from-literal MODEL_AUTH_TOKEN='Bearer <Auth token>' \
--from-literal WD_URL=<Watson Discovery URL> \
--from-literal WD_AUTH_KEY=<Watson Discovery authentication key> \
--from-literal WD_PROJECT_ID='<Watson Discovery project id>' \
--from-literal WD_COLLECTION_ID='<Watson Discovery collection id>' \
--from-literal SOLR_BACKEND=<Solr server url> \
--from-literal RERANKER_URL=<Reranker server url> \
--from-literal MONGO_URL='<MONGODB Server url>' \
--from-literal MONGO_PASS='<MongoDB password>' \
--from-literal MONGO_DB=<MongoDB Database name> \
--from-literal ELASTIC_URL='<Elasticsearch url with user and password>'
```

### Create a secret for mongodb certificate and elasticsearch certificate

```sh
oc create secret generic superknowa-ca-certificate \
--from-file elastic.crt=cert/elastic.crt \
--from-file mongo.crt=cert/mongo.crt
```

## 3. Deploy Applications

```sh
cd .../Deployment
```

```sh
oc apply -f deployment.yaml
```

```sh
oc apply -f services.yaml
```
