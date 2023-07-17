# SuperKnowa

## Generative Question & Answer on Private Knowledge Base using RAG(Retriever Augmented Generation)

RAG (Retriever Augmented Generation) uses a private enterprise knowledge base (like support documentation, books, contract documents, and corporate policy) to retrieve relevant parts using a neural search and use it to generate cogent & fluent output using LLM. A simple Q&A pipeline using APIs does not perform well in practice on accuracy metrics of specific Q&A and requires dedicated efforts. This repo covers the build of end to end pipeline to get generative output from multiple source documents.



## Single-Turn RAG(Retriver Augmented Generation)

<img src="https://media.giphy.com/media/AmvB3Wwox8JqXqrd1k/giphy.gif" alt="GIF Description" width="600" height="400">

Ml Pipeline

![image](https://github.com/EnterpriseLLM/SuperKnowa/assets/21246183/142dd017-c46a-4506-aaea-3a0dea61cebb)

1. [Data Collection](/1.%20Data%20Collection/)
2. [Indexing Documents](/2.%20Indexing%20documents/)
3. [Neural Retriever](/3.%20Neural%20Retriever/)
4. [Re-Ranker](/3.%20Neural%20Retriever/)
5. [In-context learning using LLM](/5.%20In-context%20learning%20using%20LLM/)
6. [Fine-Tuning](/7.%20Fine-Tuning/)
   1. Instruct DB
   2. Fine Tuning using QLORA
   3. Finetuning Falcon 7B
   4. Finetune OpenLAMA
   5. Finetune Flan-T5
7. [LLM Model Evaluation](/6.%20LLM%20Model%20Evaluations/)
   I. LLM Eval Toolkit <br />
   II. MLFLOW Integration <br />
   III. Benchmark on QuAC <br />
   IV. Benchmark on SqUAD <br />
   V. Benchmark on CoQA <br />
   VI. Benchmark on TydiQA <br />
   VII. Benchmark on Dolly <br />
8. [Feedback & Reward Model](/7.%20Feedback%20%26%20Reward%20Model/)
9. [User Application](/9.%20User%20Application/)

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

Copyright-
