# Re-Ranker Module

![ColBERT Framework](https://raw.githubusercontent.com/stanford-futuredata/ColBERT/master/docs/images/ColBERT-Framework-MaxSim-W370px.png)

Source:https://www.semanticscholar.org/paper/ColBERT%3A-Efficient-and-Effective-Passage-Search-via-Khattab-Zaharia/60b8ad6177230ad5402af409a6edb5af441baeb4

This directory consists of code implementations for retrieving data (from Solr, Watson Discovery and Elasticsearch) and applying the Re-Ranking algorithm to create a more efficient search result. This example demonstrates ColBert based **DrDecr reranker model** here but you can also replace it with any other re-ranking model such as **Perplexity ranking model**.

## Directory Content:

### Elasticsearch
- Elastic retriever has various models to improve the relevancy of the returned document.
    1. [es_retriever_reranker.ipynb](../3.%20Re-ranker/Elastic%20Search/es_%20reteriver_reranker.ipynb): This Jupyter notebook explains the process of retrieving data from the ES index and applying the Colbert based DrDecr re-Ranker algorithm using a Deep learning model.

### Solr <img src="https://norconex.com/wp-content/uploads/Solr_Logo_on_white_web.png" height="50" width="50"> 
- Solr retrieval works best for really long documents like books with hundreds of pages. 
    1. [solr_retriever_reranker.ipynb](../3.%20Re-ranker/Solr/solr_retriever_reranker.ipynb): This Jupyter notebook explains the process of retrieving data from the Solr database and applying the Colbert Re-Ranker algorithm using a Deep learning model.
    2. [solr_retriever_reranker.py](../3.%20Re-ranker/Solr/solr_retriever_reranker.py): This Python script programmatically retrieves data from the Solr database and applies the Colbert Re-Ranker algorithm using a Deep learning model.

### Watson Discovery <img src="https://www.cloudcreations.com/wp-content/uploads/2020/10/icon_ibmwatson_5.png" height="50" width="50"> 

1. [Re-ranker.ipynb](../3.%20Re-ranker/Watson%20Discovery/Re-ranker.ipynb): This Jupyter notebook outlines the data retrieval process from Watson Discovery and the subsequent application of the Colbert Re-Ranker algorithm.

### [Reranker.py](./reranker.py): 
Reusable script to rank  and get document that is the closest match to given query. 

These scripts and notebooks are  helpful guidebooks. They demonstrate how to pull data from different places and make your search results better by using something called the re-ranking algorithm. This algorithm considers how closely a query matches and the data quality, to ensure the best possible results.

## Getting Started

1. Clone this repository.
2. Modify the [config.yaml](../config.yaml) to update the `reranker` model if required
3. Run the [reranker.py](./reranker.py) to see the Reranker module in action.

## Reference
[DrDecr Re-ranking model](https://huggingface.co/PrimeQA/DrDecr_XOR-TyDi_whitebox)
