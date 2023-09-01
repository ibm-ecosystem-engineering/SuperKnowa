# SuperKnowa 

**Fast Framework to build Enterprise RAG (Retriever Augmented Generation) Pipelines at Scale - powered by watsonx**

Welcome to the SuperKnowa GitHub repository! SuperKnowa framework accelerates your Enterprise Generative AI applications to get prod-ready solutions quickly on your private data. Here, you will find a diverse collection of pluggable components designed to tackle various Generative AI use cases using Large Language Models (LLMs). Think of these components as building blocks, much like Lego pieces, that you can assemble to address a wide range of challenges in the realm of AI-driven text generation. These are battle-tested from 1M to 200M private knowledge base & scaled to billions of retriever tokens. 

The overall pipeline of the SuperKnowa RAG framework & key building blocks:

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWxqd3FvdHYwcnllNWt3Y2k4OHl2bXV2NHN6M21sM3Z2ZXRncmY3NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/c1v4nFUXthHQUH1EEE/giphy.gif" alt="GIF Description" width="500" height="300">

Configurable components for the SuperKnowa RAG pipeline using a single file:

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjZpZXlpMGxxODZqdHhqYm90YXVzYmIxdHlyeG9tcWg2YXhxcW5hcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QM8szBdDLn7dT90CV6/giphy.gif" alt="GIF Description" width="500" height="300">

SuperKnowa is a powerful framework developed using watsonx (watch the video on watsonx.ai [here](https://cdnapisec.kaltura.com/index.php/extwidget/preview/partner_id/1773841/uiconf_id/27941801/entry_id/1_yola7kmy/embed/dynamic)) that harnesses the capabilities of Large Language Models (LLMs) to offer a range of advanced Generative AI use cases. This repository introduces you to the various use cases covered by SuperKnowa.


📖 Learn more about SuperKnowa in our insightful blog post:


Cover Blog - SuperKnowa: Building Enterprise RAG Solutions at Scale https://medium.com/towards-generative-ai/superknowa-simplest-framework-yet-to-swiftly-build-enterprise-rag-solutions-at-scale-ca90b49be28a



###  Application for Live Q&A On Private Knowledge Base 

Try the SuperKnowa framework with a live application built on the private knowledge base of 1M diverse docs:


[https://superknowa.tsglwatson.buildlab.cloud/](https://superknowa.tsglwatson.buildlab.cloud/)


(In case you don't have IBM ID, please get it here - https://www.ibm.com/account/reg/us-en/signup?formid=urx-19776) 

## Getting Started

You can get started by updating the [`config.yaml`](./config.yaml) file and run the [LLMQnA.py](./4.%20In-context%20learning%20using%20LLM/LLMQnA.py) script for quickly configuring your RAG pipeline:

```
retriever:
  indexName: superknowa
  query: What is IBM Cloud?
  ....

reranker:
  query: What is IBM Data and Analytics Reference Architecture?
  ...

LLMQnA:
  question: What is IBM Data and Analytics Reference Architecture?
  ...
```

To explore SuperKnowa's features and capabilities, refer to the [blog series](https://medium.com/towards-generative-ai/unleashing-the-power-of-the-information-retriever-in-the-retrieval-augmented-generation-pipeline-a782c7287e9b), code examples, and resources provided in this repository.

For detailed instructions and examples, navigate to each component's directory. Unleash the potential of Large Language Models in your projects using SuperKnowa's Generative AI Lego Components!

Let's unlock the potential of Generative AI with SuperKnowa and shape the future of AI-powered knowledge processing!


# Repository Contents

1. [Indexing Documents](/1.%20Indexing%20documents/)

   1. [Elastic Search](./1.%20Indexing%20documents/Elastic%20Search/)

   1. [Solr](./1.%20Indexing%20documents/Solr/)
      
   3. Watson Discovery

1. [Neural Retriever](/2.%20Neural%20Retriever/)

   1. [Elastic Search](./2.%20Neural%20Retriever/ElasticSearch/)

   1. [Solr](./2.%20Neural%20Retriever/Solr/)

1. [Re-Ranker](/3.%20Re-ranker/)

1. [In-context learning using LLM](/4.%20In-context%20learning%20using%20LLM/)

1. [LLM Evaluations](./5.%20LLM%20Model%20Evaluations/)

   1. [LLM Model Evaluation](/5.%20LLM%20Model%20Evaluations/I.%20LLM%20Eval%20Toolkit/)

   1. [MLFLOW Integration](/5.%20LLM%20Model%20Evaluations/II.%20MLFLOW%20Integration/)

1. [Fine-Tuning](/6.%20Fine-Tuning/)

   1. [Instruct DB](./6.%20Fine-Tuning/1.%20Instruct%20DB/)

   1. [Fine Tuning Falcon 7B using QLORA](./6.%20Fine-Tuning/2.%20Falcon-7B/)
   2. Fine Tuning LLAMA2 7B using QLORA

1. [RLHF Model](./7.%20RLHF%20Model/)

1. [Deploy & Infer](./8.%20Deploy%20%26%20Infer/)

   1. [Backend](./8.%20Deploy%20%26%20Infer/Backend/)

   1. [Deployment](./8.%20Deploy%20%26%20Infer/Deployment/)

1. [AI Alignment Tool](./9.%20AI%20Alignment%20Tool/)
   1. Capture Human Feedback
   2. Admin Dashboard for AI Alignment Results

1. [Enterprise LLM Use Cases](./Enterprise%20LLM%20Use%20Cases/)


## AI Alignment Tool  
Measure the alignment of AI models on the metrics of helpfulness, harmfulness and accuracy by capturing human inputs. 

### Results Dashboard
Build your various online & offline experiments for evaluations and compare the AI alignment results using an interactive dashboard. 



<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW1jeW82cWRtemo5cHN5dm0yMGFyazR5ajY5M2J1ZnNiNGkwenF2ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Q4V3CoTxQ5jJqbIuWp/giphy.gif" alt="GIF Description" width="500" height="300">



## LLM Eval Toolkit 

### [Eval_Package](5.%20LLM%20Model%20Evaluations/I.%20LLM%20Eval%20Toolkit/Eval_Package)
  
The Eval_Package is a tool designed to evaluate the performance of the LLM (Language Model) on a dataset containing questions, context, and ideal answers. It allows you to run evaluations on various datasets and assess how well the Model generates the answer on dozens of statistical metrics like BLUE, ROUGE, etc. 


### Features 
   - Evaluate LLM Model on custom datasets: Use the Eval_Package to assess the performance of your Model on datasets of your choice.
   - Measure model accuracy: The package provides metrics to gauge the accuracy of the model-generated answers against the ideal answers.

## [MLflow_Package](5.%20LLM%20Model%20Evaluations/I.%20LLM%20Eval%20Toolkit/mlflow_package)

The MLflow_Package is a comprehensive toolkit designed to integrate the results from the Eval_Package and efficiently track and manage experiments. It also enables you to create a leaderboard for evaluation comparisons and visualize metrics through a dashboard.

### Features 
   - Statistical Metrics Supported are BLEU, METEOR, ROUGE, SentenceSim Score, SimHash Score, Perplexity Score, BLEURT Score, F1 Score and BERT score.
   - Experiment tracking: Utilize MLflow to keep a record of experiments, including parameters, metrics, and model artifacts generated during evaluations.
   - Leaderboard creation: The package allows you to create a leaderboard, making it easy to compare the performance of different  Models across multiple datasets.
   - Metric visualization: Generate insightful charts and graphs through the dashboard, allowing you to visualize and analyze evaluation metrics easily.


# Enterprise LLM Use Cases

Below is a list of Generative AI use cases built using the SuperKnowa framework.

### 1. Conversational Q&A on Private Knowledge Base
Engage in natural language conversations with SuperKnowa's conversational Question & Answer (Q&A) system. Ask questions based on the private enterprise knowledge base, and receive detailed, context-aware responses.

<img src="https://media.giphy.com/media/AmvB3Wwox8JqXqrd1k/giphy.gif" alt="GIF Description" width="500" height="300">

### 2. Ask Your PDF/Documents
Leverage SuperKnowa's "Ask your documents" feature to unlock the potential of your PDFs and text documents. SuperKnowa can help you extract relevant information, answer specific questions, and assist in information retrieval.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGJtb3gzbmZpcHFycGd5NXlwZTNnenFldXVzNnlqd2x4Z2w2ZWxkbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RHiZsJJMAGURFWplHL/giphy.gif" alt="SuperKnowa PDF version"
width="500" height="300">

### 3. Summarisation
Effortlessly generate coherent and informative summaries with SuperKnowa's summarization feature across large text corpus using FlanT5 and UL2. Extract the main points and essential details from articles, reports, and other texts, allowing for efficient content comprehension.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTk3NWJtczFsaGp6aXd2Z2hoM3pzeHNwcm1ocWVvOHZjeGJubzh2YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5Z5wAc62XXZNlCgvOO/giphy.gif" alt="SuperKnowa PDF version"
width="500" height="300">

### 4. Key Points from your PDF
SuperKnowa's abstractive summarisation feature goes beyond simple extraction using FlanUL2, and LLAMA2. It can analyze lengthy PDF documents and generate concise abstractive summaries, capturing the essence of the content. Additionally, SuperKnowa identifies key points, making it easier to comprehend and communicate complex information.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2wyN3NjNmVsbHhoaXJ3ODRzazJ4bnU2Z2p5ZWtmcTNvY3RmNjN4NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tQO2UoGJO8zEuGK4OC/giphy.gif" alt="PDF Understanding" width="500" height="300">

### 5. Text to SQL
Experience the power of SuperKnowa's Text-to-SQL capability, which transforms natural language queries into structured SQL queries. Interact with databases using plain language, eliminating the need for expertise in SQL.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTV1MTF2bXdicW83ZGpqcGM3ZDA2MTluaTQ2cm1nNWFtZnkwZXdqNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XW5a5FF0wF9PudBzuz/giphy.gif" alt="GIF Description" width="500" height="300">


## Build Lab Team 

Owner: Kunal Sawarkar, Chief Data Scientist

Builders
- Shivam Solanki, Senior Advisory Data Scientist
- Michael Spriggs, Principal Architect
- Kevin Huang, Sr. ML-Ops Engineer 
- Abhilasha Mangal, Senior Data Scientist
- Sahil Desai, Data Scientist
- Amit Khandelwal- Senior Data Scientist
- Himadri Talukder - Senior Software Engineer
- Tyler Berns- Data Scientist

  

### Disclaimer 
This framework is developed by Build Lab, IBM Ecosystem. Please note that this content is made available to foster Embeddable AI technology adoption and serve ecosystem partners. The content may include systems & methods pending patent with the USPTO and protected under US Patent Laws. SuperKnowa is not a product but a framework built on the top of IBM watsonx along with other products like LLAMA models from Meta & ML Flow from Databricks. Using SuperKnowa implicitly requires agreeing to the Terms and conditions of those products. This framework is made available on an as-is basis to accelerate Enterprise GenAI applications development. In case of any questions, please reach out to kunal@ibm.com.  


Copyright @ 2023 IBM Corporation. 
