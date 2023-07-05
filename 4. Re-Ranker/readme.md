# Re-Ranker

This folder contains code for retrieving data from Solr and Watson Discovery and apply Re-Ranker algorithm :

- [Solr](../4. Re-Ranker/Solr/): Retrieving data from SOLR
    - [solr_retriever_reranker.ipynb](../4. Re-Ranker/Solr/solr_retriever_reranker.ipynb): Reterving data from solr and apply Colbert Reranker on data with single LLM model
    - [solr_retriever_reranker.py](../4. Re-Ranker/Solr/solr_retriever_reranker.py): Reterving data from solr and apply Colbert Reranker on data with single LLM model
    - [solr_three_models.py](../4. Re-Ranker/Solr/solr_three_models.py): Reterving data from solr and applying Colbert Reranker on data with 3 LLM models
    
- [Watson Discovery](../4. Re-Ranker/Watson Discovery/): Retrieving data from Watson Discovery 
    - [Re-ranker.ipynb](../4. Re-Ranker/Watson Discovery/Re-ranker.ipynb): Reterving data from Watson Discovery and apply Colbert Reranker on data with single LLM model
