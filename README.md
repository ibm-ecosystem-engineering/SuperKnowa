# SuperKnowa

## Generative Question & Answer for Enterprise Private Knowledge Base

RAG (Retriever Augmented Generation) uses a private enterprise knowledge base (like support documentation, books, contract documents, and corporate policy) to retrieve relevant parts using a neural search and use it to generate cogent & fluent output using LLM. A simple Q&A pipeline using APIs does not perform well in practice on accuracy metrics of specific Q&A and requires dedicated efforts. This repo covers the build of end to end pipeline to get generative output from multiple source documents.



## Single-Turn RAG(Retriver Augmented Generation)

Ml Pipeline

![image](https://github.com/EnterpriseLLM/SuperKnowa/assets/21246183/142dd017-c46a-4506-aaea-3a0dea61cebb)



1. Data Collection
2. Search Index
3. Neural Retriever
4. Re-Ranker
5. In-context learning using LLM <br />
   BLOOM <br />
   BLOOMChat <br />
7. LLM Model Evaluation <br />
   I. LLM Eval Toolkit <br />
   II. MLFLOW Integration <br />
   III. Benchmark on QuAC <br />
   IV. Bechmark on SqUAD <br />
   V. Bechmark on CoQA
8. Feedback & Reward Model
9. User Application

## Fine-Tuning
1. Instruct DB
2. Fine Tuning using QLORA
3. Finetuning Falcon 7B
4. Finetune OpenLAMA
5. Finetune Flan-T5
6. Finetune Coga


## Knowledge Graph with LLM
1. KG with FlanT5
2. 

===================================

Owner

Kunal Sawarkar

Build Team 

- Shivam Solanki- Senior Data Scientist
- Abhilasha Mangal- Senior Data Scientist
- Sahil Desai- Senior Data Scientist
- Amit Khandelwal- Senior Data Scientist

Copyright-
