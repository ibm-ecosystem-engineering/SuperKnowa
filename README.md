# SuperKnowa powered by watsonx.ai
- <add a generic intro> 
- Text to SQL
- Converaational Q&A
- Ask your documents (like pdf)
- Abstractive Summarisation & Key Points from your pdf
- Summarisation

## Generative Question & Answer on Private Knowledge Base using RAG(Retriever Augmented Generation)

RAG (Retriever Augmented Generation) uses a private enterprise knowledge base (like support documentation, books, contract documents, and corporate policy) to retrieve relevant parts using a neural search and use it to generate cogent & fluent output using LLM. A simple Q&A pipeline using APIs does not perform well in practice on accuracy metrics of specific Q&A and requires dedicated efforts. This repo covers the build of end to end pipeline to get generative output from multiple source documents.



## Single-Turn RAG(Retriver Augmented Generation)

Watch the video on watsonx.ai [here](https://cdnapisec.kaltura.com/index.php/extwidget/preview/partner_id/1773841/uiconf_id/27941801/entry_id/1_yola7kmy/embed/dynamic).


<img src="https://media.giphy.com/media/AmvB3Wwox8JqXqrd1k/giphy.gif" alt="GIF Description" width="600" height="400">

Ml Pipeline

![image](https://github.com/EnterpriseLLM/SuperKnowa/assets/21246183/142dd017-c46a-4506-aaea-3a0dea61cebb)

## [Evaluation Leaderboard](./5.%20LLM%20Model%20Evaluations/II.%20MLFLOW%20Integration/)


- flan-t5-xxl outperforms ul2 irrespective of retriever used
- ES scores better in comparison to Solr as retriever for flan-t5-xxl
- There is a drop in accuracy when we use reranker in comparsion to when we do not.


![Screenshot 2023-07-31 at 8 55 13 PM](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/d34c6e55-0fb8-4636-82ff-b4f57ff56ef8)


![visualization](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/58d6e72b-c40f-4a3c-9d01-7fe1d191e583)


![visualization (2)](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/13d75f46-04ad-4c78-a9fb-833a2f2f4299)

## RAG Evaluation packages 

## [Eval_Package](5.%20LLM%20Model%20Evaluations/I.%20LLM%20Eval%20Toolkit/Eval_Package)
  
The Eval_Package is a tool designed to evaluate the performance of the LLM (Language Model) on a dataset containing questions, context, and ideal answers. It allows you to run evaluations on various datasets and assess how well the Model generates the answer.

### Features 
   - Evaluate LLM Model on custom datasets: Use the Eval_Package to assess the performance of your Model on datasets of your choice.
   - Measure model accuracy: The package provides metrics to gauge the accuracy of the model-generated answers against the ideal answers.

## [MLflow_Package](5.%20LLM%20Model%20Evaluations/I.%20LLM%20Eval%20Toolkit/mlflow_package)

The MLflow_Package is a comprehensive toolkit designed to integrate the results from the Eval_Package and efficiently track and manage experiments. It also enables you to create a leaderboard for evaluation comparisons and visualize metrics through a dashboard.

### Features 
   - Experiment tracking: Utilize MLflow to keep a record of experiments, including parameters, metrics, and model artifacts generated during evaluations.
   - Leaderboard creation: The package allows you to create a leaderboard, making it easy to compare the performance of different  Models across multiple datasets.
   - Metric visualization: Generate insightful charts and graphs through the dashboard, allowing you to visualize and analyze evaluation metrics easily.

===================================

## Repository Contents

1. [Indexing Documents](/1.%20Indexing%20documents/)

   1. [Elastic Search](./1.%20Indexing%20documents/Elastic%20Search/)

   1. [Solr](./1.%20Indexing%20documents/Solr/)

1. [Neural Retriever](/2.%20Neural%20Retriever/)

   1. [Elastic Search](./2.%20Neural%20Retriever/ElasticSearch/)

   1. [Solr](./2.%20Neural%20Retriever/Solr/)

1. [Re-Ranker](/3.%20Re-ranker/)

1. [In-context learning using LLM](/4.%20In-context%20learning%20using%20LLM/)

1. [LLM Model Evaluation](/5.%20LLM%20Model%20Evaluations/)

   1. [LLM Eval Toolkit](/5.%20LLM%20Model%20Evaluations/I.%20LLM%20Eval%20Toolkit/)

   1. [MLFLOW Integration](/5.%20LLM%20Model%20Evaluations/II.%20MLFLOW%20Integration/)

   1. [Benchmark Evaluation](./5.%20LLM%20Model%20Evaluations/III.%20Benchmark%20Evaluations/)

1. [Fine-Tuning](/6.%20Fine-Tuning/)

   1. [Instruct DB](./6.%20Fine-Tuning/1.%20Instruct%20DB/)

   1. [Fine Tuning Falcon 7B using QLORA](./6.%20Fine-Tuning/2.%20Falcon-7B/)

1. [Feedback & Reward Model](/7.%20Feedback%20%26%20Reward%20Model/)

1. [User Application](/9.%20User%20Application/)

   1. [Backend](./8.%20Application/Backend/)

   1. [Deployment](./8.%20Application/Deployment/)

===================================

Owner: Kunal Sawarkar

Build Team 

- Shivam Solanki- Senior Advisory Data Scientist
- Abhilasha Mangal- Senior Data Scientist
- Sahil Desai- Senior Data Scientist
- Amit Khandelwal- Senior Data Scientist
- Himadri Talukder - Senior Software Engineer
