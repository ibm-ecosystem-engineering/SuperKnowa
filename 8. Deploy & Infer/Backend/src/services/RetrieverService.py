from src.config.Config import Config
import time
from src.solr.ProcessSolr import ProcessSolr
from src.services.ModelConfig import ModelConfig
from src.elastic.ProcessElastic import ProcessElastic
import pandas as pd

class RetrieverService:
    
    def __init__(self) -> None:
        pass

    def retrieve_documents(self, info, question, retriever ):
        config = Config()
        if(retriever == "elastic"):
            elastic = ProcessElastic()
            tic = time.perf_counter()
            results_list = elastic.elastic_retervier(question)
            toc = time.perf_counter()
            duration = toc - tic
            info['elastic_query_time'] = duration
            info['elastic_result'] = results_list

            results_to_display = [results_list['document'] for results_list in results_list]
            df = pd.DataFrame.from_records(results_to_display, columns=['rank','document_id','text','url','source'])
            df.dropna(inplace=True)
            
        elif(retriever == "solr"):
            solr = ProcessSolr()
            tic = time.perf_counter()
            results_list = solr.solr_reteriver(question, info)
            toc = time.perf_counter()
            duration = toc - tic
            info['solr_query_time'] = duration
            info['solr_result'] = results_list
    
        tic = time.perf_counter()
        context, source_url = config.reranking(question=question, results_list=results_list, max_reranked_documents=10)
        info['source_url'] = source_url
        toc = time.perf_counter()
        duration = toc - tic
        info['reranker_load_time'] = duration
        print(f"Reranker load time ==> {toc - tic:0.4f} seconds")
        return context, source_url