# SuperKnowa powered by watsonx.ai

Welcome to the SuperKnowa GitHub Repository!

SuperKnowa is a powerful platform developed by watsonx.ai (watch the video on watsonx.ai [here](https://cdnapisec.kaltura.com/index.php/extwidget/preview/partner_id/1773841/uiconf_id/27941801/entry_id/1_yola7kmy/embed/dynamic)) that harnesses the capabilities of Large Language Models (LLMs) to offer a range of advanced Generative AI use cases. This repository introduces you to the various use cases covered by SuperKnowa.

## Use Cases
### Conversational Q&A
Engage in natural language conversations with SuperKnowa's conversational Question & Answer (Q&A) system. Ask questions based on private enterprise knowledge base, and receive detailed, context-aware responses.

### Ask Your Documents
Leverage SuperKnowa's "Ask your documents" feature to unlock the potential of your PDFs and text documents. SuperKnowa can help you extract relevant information, answer specific questions, and assist in information retrieval.

### Abstractive Summarisation & Key Points from PDF
SuperKnowa's abstractive summarisation feature goes beyond simple extraction. It can analyze lengthy PDF documents and generate concise abstractive summaries, capturing the essence of the content. Additionally, SuperKnowa identifies key points, making it easier to comprehend and communicate complex information.

### Summarisation
Effortlessly generate coherent and informative summaries with SuperKnowa's summarisation feature. Extract the main points and essential details from articles, reports, and other texts, allowing for efficient content comprehension.

### Text to SQL
Experience the power of SuperKnowa's Text to SQL capability, which transforms natural language queries into structured SQL queries. Interact with databases using plain language, eliminating the need for expertise in SQL.

## Getting Started
To explore SuperKnowa's features and capabilities, refer to the [blog series](https://medium.com/towards-generative-ai/unleashing-the-power-of-the-information-retriever-in-the-retrieval-augmented-generation-pipeline-a782c7287e9b), code examples, and resources provided in this repository.

For questions, feedback, or collaboration opportunities, feel free to reach out to us.

Let's unlock the potential of Generative AI with SuperKnowa and shape the future of AI-powered knowledge processing!

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

1. [Generative AI use cases]()

============================================================================

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

Owner: Kunal Sawarkar

Build Team 

- Shivam Solanki- Senior Advisory Data Scientist
- Abhilasha Mangal- Senior Data Scientist
- Sahil Desai- Senior Data Scientist
- Amit Khandelwal- Senior Data Scientist
- Himadri Talukder - Senior Software Engineer
