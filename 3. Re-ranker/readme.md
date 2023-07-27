# Re-Ranker Module

![ColBERT Framework](https://raw.githubusercontent.com/stanford-futuredata/ColBERT/master/docs/images/ColBERT-Framework-MaxSim-W370px.png)

Source:https://www.semanticscholar.org/paper/ColBERT%3A-Efficient-and-Effective-Passage-Search-via-Khattab-Zaharia/60b8ad6177230ad5402af409a6edb5af441baeb4

The `Re-Ranker` module consists of code implementations for retrieving data (from Solr, Watson Discovery and Elastic Search databases) and applying the Re-Ranking algorithm to create a more efficient search result.

This folder is structured as follows:


## Watson Discovery <img src="https://www.cloudcreations.com/wp-content/uploads/2020/10/icon_ibmwatson_5.png" height="50" width="50"> 
- **Retrieval and Re-ranking with Watson Discovery**
    1. [Re-ranker.ipynb](../4.%20Re-Ranker/Watson%20Discovery/Re-ranker.ipynb): This Jupyter notebook outlines the data retrieval process from Watson Discovery and the subsequent application of the Colbert Re-Ranker algorithm.

These scripts and notebooks are  helpful guidebooks. They show you how to pull data from different places and make your search results better by using something called the re-ranking algorithm. They take into account how closely a query matches and how good the data is to make sure the results are the best they can be.

## Solr <img src="https://norconex.com/wp-content/uploads/Solr_Logo_on_white_web.png" height="50" width="50"> 
- **Retrieval and Re-ranking with Solr**
- Solr retrieval works best for really long documents like books with hundreds of pages. 
    1. [solr_retriever_reranker.ipynb](../4.%20Re-Ranker/Solr/solr_retriever_reranker.ipynb): This Jupyter notebook explains the process of retrieving data from the Solr database and applying the Colbert Re-Ranker algorithm using a Deep learning model.
    2. [solr_retriever_reranker.py](../4.%20Re-Ranker/Solr/solr_retriever_reranker.py): This Python script programmatically retrieves data from the Solr database and applies the Colbert Re-Ranker algorithm using a Deep learning model.


## Elastic
- **Retrieval and Re-ranking with Elastic Search**
- Elastic retriever has various models to improve the relevancy of the returned document.
    1. [es_retriever_reranker.ipynb](../3.%20Re-ranker/Elastic%20Search/es_%20reteriver_reranker.ipynb): This Jupyter notebook explains the process of retrieving data from the ES index and applying the Colbert based DrDecr re-Ranker algorithm using a Deep learning model.

## Reference
[DrDecr Re-ranking model](https://huggingface.co/PrimeQA/DrDecr_XOR-TyDi_whitebox)