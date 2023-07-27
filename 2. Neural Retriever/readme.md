# Information Retriever for Retrieval Augmented Generation

This repository contains Python scripts demonstrating the use of a Neural Retriever in a Retrieval Augmented Generation (RAG) pipeline. The scripts demonstrate three different implementations of a Neural Retriever using Apache Solr, Elasticsearch, and Wikidata as document stores.

## Directory Contents

- [Elastic Search](../3.%20Neural%20Retriever/ElasticSearch/): Demonstrates the use of Elasticsearch as a document store for the neural retriever.
    - [es_retriever.ipynb](../3.%20Neural%20Retriever/ElasticSearch/es_retriever.ipynb): Notebook for retrieving documents from the Elastic Search index
- [Solr](../3.%20Neural%20Retriever/Solr/): Demonstrates the use of Apache Solr as a document store for the neural retriever.
    - [solr_retriever.ipynb](../3.%20Neural%20Retriever/Solr/solr_retriever.ipynb): An example notebook showing how to query documents from the Solr collection
    - [solr_retriever](../3.%20Neural%20Retriever/Solr/solr_retriever.py): Python Script to search for documents from the Solr indexed collection

- [Watson Discover](../3.%20Neural%20Retriever/Watson%20Discovery/): Demonstrates the use of Watson Discovery as a document store for the neural retriever.
    - [WD_PDF_Retriever](../3.%20Neural%20Retriever/Watson%20Discovery/WD_PDF_Retriever.py): A Python scripts that uploads and indexes a PDF to the Watson Discovery collection making it available for future queries
    - [WD_retriever.py](../3.%20Neural%20Retriever/Watson%20Discovery/WD_retriever.py): A Python script for querying documents from the Watson Discovery collection.
    
![Retriever](./Screenshots/retriever.png)

## Getting Started

1. Clone this repository.
2. Install the required dependencies (see the Dependencies section below).
3. Update the document store connection details in the scripts as necessary.
4. Run the desired script to see the neural retriever in action.

## Usage

Each script defines a function for the information retriever (`SolrRetriever`, `ESRetriever`, or `WDRetriever`) takes a query and returns the top matching documents from the respective document store.

Here's a basic example of how you might use the `SolrRetriever`:

```python
retriever = SolrRetriever(solr_url='http://localhost:8983/solr', collection_name='my_collection')
results = retriever.retrieve('What is DataOps?')
print(results)
```

## Dependencies

These scripts require Python 3.6 or later. They also require the following Python libraries:

- `pysolr` (for `solr_retriever.py`)
- `elasticsearch` (for `es_retriever.ipynb`)
- `requests` (for `wd_retriever.py`)

You can install these libraries using pip:

```
pip install pysolr elasticsearch requests
```
