# SuperKnowa

## Generative Question & Answer on Private Knowledge Base using RAG(Retriever Augmented Generation)

RAG (Retriever Augmented Generation) uses a private enterprise knowledge base (like support documentation, books, contract documents, and corporate policy) to retrieve relevant parts using a neural search and use it to generate cogent & fluent output using LLM. A simple Q&A pipeline using APIs does not perform well in practice on accuracy metrics of specific Q&A and requires dedicated efforts. This repo covers the build of end to end pipeline to get generative output from multiple source documents.



## Single-Turn RAG(Retriver Augmented Generation)

Watch the video [here](https://cdnapisec.kaltura.com/index.php/extwidget/preview/partner_id/1773841/uiconf_id/27941801/entry_id/1_yola7kmy/embed/dynamic).


<img src="https://media.giphy.com/media/AmvB3Wwox8JqXqrd1k/giphy.gif" alt="GIF Description" width="600" height="400">

Ml Pipeline

![image](https://github.com/EnterpriseLLM/SuperKnowa/assets/21246183/142dd017-c46a-4506-aaea-3a0dea61cebb)

Evaluation Leaderboard


- flan-t5-xxl outperforms ul2 irrespective of retriever used
- ES scores better in comparison to Solr as retriever for flan-t5-xxl
- There is a drop in accuracy when we use reranker in comparsion to when we do not.


![Screenshot 2023-07-31 at 8 55 13 PM](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/d34c6e55-0fb8-4636-82ff-b4f57ff56ef8)


![visualization](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/58d6e72b-c40f-4a3c-9d01-7fe1d191e583)


![visualization (2)](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/13d75f46-04ad-4c78-a9fb-833a2f2f4299)


1. [Indexing Documents](/1.%20Indexing%20documents/)
1. [Neural Retriever](/2.%20Neural%20Retriever/)
1. [Re-Ranker](/3.%20Re-ranker/)
1. [In-context learning using LLM](/4.%20In-context%20learning%20using%20LLM/)
1. [LLM Model Evaluation](/5.%20LLM%20Model%20Evaluations/)  <br />
   I. LLM Eval Toolkit <br />
   II. MLFLOW Integration <br />
   III. Benchmark on QuAC <br />
   IV. Benchmark on SqUAD <br />
   V. Benchmark on CoQA <br />
   VI. Benchmark on TydiQA <br />
   VII. Benchmark on Dolly <br />
1. [Fine-Tuning](/6.%20Fine-Tuning/)
   1. Instruct DB
   2. Fine Tuning using QLORA
   3. Finetuning Falcon 7B
   4. Finetune OpenLAMA
   5. Finetune Flan-T5
1. [Feedback & Reward Model](/7.%20Feedback%20%26%20Reward%20Model/)
1. [User Application](/9.%20User%20Application/)

===================================
## Knowledge Graph with LLM
1. KG with FlanT5
2. 
===================================


Owner

Kunal Sawarkar

Build Team 

- Shivam Solanki- Senior Advisory Data Scientist
- Abhilasha Mangal- Senior Data Scientist
- Sahil Desai- Senior Data Scientist
- Amit Khandelwal- Senior Data Scientist
- Himadri Talukder - Senior Software Engineer

Copyright-
