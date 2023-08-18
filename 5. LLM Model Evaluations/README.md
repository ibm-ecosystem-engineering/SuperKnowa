# RAG evaluation packages

<img src="https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/23766e0c-a39c-4139-ad78-a7c9ad2420cf" alt="image" width="700" height="300">

## [Eval_Package](./I.%20LLM%20Eval%20Toolkit/Eval_Package/)
  
The Eval_Package is a tool designed to evaluate the performance of the LLM (Language Model) on a dataset containing questions, context, and ideal answers. It allows you to run evaluations on various datasets and assess how well the Model generates the answer.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTllNWVhYTdsYjZrZHFqeDhzcXcwcDlqcWs0ajJnZHVhNGYyZW9pMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2ZN76vTSwlqxbwcpjX/giphy.gif" alt="GIF Description" width="500" height="300">

### Features 
   - Evaluate LLM Model on custom datasets: Use the Eval_Package to assess the performance of your Model on datasets of your choice.
   - Measure model accuracy: The package provides metrics to gauge the accuracy of the model-generated answers against the ideal answers.

## [MLflow_Package](./I.%20LLM%20Eval%20Toolkit/mlflow_package/)

The MLflow_Package is a comprehensive toolkit designed to integrate the results from the Eval_Package and efficiently track and manage experiments. It also enables you to create a leaderboard for evaluation comparisons and visualize metrics through a dashboard.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjJod3pnZG1hbjloano0cmhxZ3JrbDJsbXgxM2t5enF5eXI3cWZvaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6FV33YFa0HxuDxjPv9/giphy.gif" alt="GIF Description" width="500" height="300">

 # Experiment Visualization using Leaderboard

### Features 

   - **Experiment tracking:** Use MLflow to keep a record of experiments, including parameters, metrics, and model artifacts generated during evaluations.
   - **Leaderboard creation:** The package allows you to create a leaderboard, making it easy to compare the performance of different  Models across multiple datasets.
   - **Metric visualization:** Generate insightful charts and graphs through the dashboard, allowing you to visualize and analyze evaluation metrics easily.

![ML-Flow-Dashboard](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/2b3ca47b-e779-4411-8c8a-2d4715bdc9fe)

## Directory contents

-  [I. LLM Eval Toolkit](I.%20LLM%20Eval%20Toolkit): Toolkit for evaluating RAG pipeline

   1. [Eval_Package](./I.%20LLM%20Eval%20Toolkit/Eval_Package/): A package to automatically evaluate the LLM based RAG pipeline
   1. [mlflow_package](./I.%20LLM%20Eval%20Toolkit/mlflow_package/): A package to automatically add the evaluation results to the



- [II. MLFLOW Integration](II.%20MLFLOW%20Integration): MLFlOW evaluation dashboard scripts
   1. [Notebook](II.%20MLFLOW%20Integration/Notebook): Evaluation Notebook
   1. [Output_CSV](II.%20MLFLOW%20Integration/Output_CSV): Output CSV for LLM Models Evaluation
   1. [Result](II.%20MLFLOW%20Integration/Result): Result file and png of MLFLOW
   1. [mlruns](II.%20MLFLOW%20Integration/mlruns): MLFLOW metadata 


