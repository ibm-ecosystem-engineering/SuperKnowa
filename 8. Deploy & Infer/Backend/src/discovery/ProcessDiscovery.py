import os
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import numpy as np
import pandas as pd
from src.config.Config import Config
import datetime
import time

class ProcessDiscovery:
    
    def __init__(self, authenticator):
        # Discovery Service Handling
        self.discovery = DiscoveryV2(
            version='2020-08-30',
            authenticator=authenticator
        )

    def WD_Retriever(self, question):
        tic = time.perf_counter()
        hits =  self.discovery.query(
                project_id=Config.project_id,
                collection_ids=[Config.collection_id],
                natural_language_query=question,
                count=Config.max_num_documents).get_result()["results"]

        #print(f'Number of hits: {len(hits)}')

        results_list = []
        if hits:
            for i, hit in enumerate(hits):
                query_hits = {
                "document": {
                    "rank": i,
                    "document_id": hit["document_id"] if "document_id" in hit else None,
                    "text": hit["text"][0][0:4000], # Only extracting first 1000 words
                    "title": hit["title"] if "title" in hit else str(np.random.randint(1, 10))
                },
                "score": hit['result_metadata']['confidence'],
                }

                results_list.append(query_hits)

        results_to_display = [results_list['document'] for results_list in results_list]
        df = pd.DataFrame.from_records(results_to_display, columns=['rank','document_id','title','text'])
        # df['title'] = np.random.randint(1, 10, df.shape[0])
        df.dropna(inplace=True)
        print('======================================================================')
        #print(f'QUERY: {question}')
        toc = time.perf_counter()
        print(f"discovery {toc - tic:0.4f} seconds")
        return results_list
    
    def WD_reranker(self, question, max_reranked_documents):
        results_list = self.WD_Retriever(question)
        config = Config()
        reranked_results = config.reranking(question=question, results_list=results_list, max_reranked_documents=max_reranked_documents)
        return reranked_results[0]