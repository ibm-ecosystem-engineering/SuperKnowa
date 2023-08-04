# LLM Model Evaluation

This folder contains LLM Model Evaluation scripts and Benchmark sample data as listed below:


<img src="https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/23766e0c-a39c-4139-ad78-a7c9ad2420cf" alt="image" width="700" height="300">

## Evaluation Process:

-   Run evaluation on Different LLM models:
   - Evaluate the Q&A generation models, including Bloom, FlanT5-XXL, and Coga, using the specified evaluation metrics.
   - Record the evaluation results for each model in separate CSV files.
- Store Result CSV Files in MLFlow Data Source:
   - Upload the result CSV files containing evaluation metrics and model information to the MLFlow data source.
   - MLFlow will automatically organize and version the evaluation results for each model run.
- Execute the MLFlow Evaluation Python Script:
   - Use the MLFlow evaluation Python script to analyze the result CSV files and calculate aggregated metrics for each model.
- MLFlow Dashboard:
   - Access the MLFlow dashboard, which provides a visual representation of the evaluation results.
   - The dashboard showcases model performance using graphs, charts, and tables, making it easier to compare and analyze the different LLM models.

![ML-Flow-Dashboard](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/2b3ca47b-e779-4411-8c8a-2d4715bdc9fe)

Evaluation Leaderboard

- flan-t5-xxl outperforms ul2 irrespective of retriever used
- ES scores better in comparison to Solr as retriever for flan-t5-xxl
- There is a drop in accuracy when we use reranker in comparsion to when we do not.


![Screenshot 2023-07-31 at 8 55 13 PM](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/d34c6e55-0fb8-4636-82ff-b4f57ff56ef8)


![visualization](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/58d6e72b-c40f-4a3c-9d01-7fe1d191e583)


![visualization (2)](https://github.com/EnterpriseLLM/SuperKnowa/assets/112084296/13d75f46-04ad-4c78-a9fb-833a2f2f4299)

## Eval_Package and MLflow_Package for Evaluation 

[Eval_Package](I.%20LLM%20Eval%20Toolkit/Eval_Package)
  
The Eval_Package is a tool designed to evaluate the performance of the LLM (Language Model) on a dataset containing questions, context, and ideal answers. It allows you to run evaluations on various datasets and assess how well the Model generates the answer.

### Features 
   - Evaluate LLM Model on custom datasets: Use the Eval_Package to assess the performance of your Model on datasets of your choice.
   - Measure model accuracy: The package provides metrics to gauge the accuracy of the model-generated answers against the ideal answers.

[MLflow_Package](I.%20LLM%20Eval%20Toolkit/MLflow_Package)

The MLflow_Package is a comprehensive toolkit designed to integrate the results from the Eval_Package and efficiently track and manage experiments. It also enables you to create a leaderboard for evaluation comparisons and visualize metrics through a dashboard.

### Features 
   - Experiment tracking: Utilize MLflow to keep a record of experiments, including parameters, metrics, and model artifacts generated during evaluations.
   - Leaderboard creation: The package allows you to create a leaderboard, making it easy to compare the performance of different  Models across multiple datasets.
   - Metric visualization: Generate insightful charts and graphs through the dashboard, allowing you to visualize and analyze evaluation metrics easily.

- [I. LLM Eval Toolkit](I.%20LLM%20Eval%20Toolkit): Scripts for LLM Model Evaluation table generation
- [II. MLFLOW Integration](II.%20MLFLOW%20Integration): MLFlOW evaluation dashboard script
   - [Notebook](II.%20MLFLOW%20Integration/Notebook): Evaluation Notebook
   - [Output_CSV](II.%20MLFLOW%20Integration/Output_CSV): Output CSV for LLM Models Evaluation
   - [Result](II.%20MLFLOW%20Integration/Result): Result file and png of MLFLOW
   - [mlruns](II.%20MLFLOW%20Integration/mlruns): MLFLOW metadata 
- [III. Benchmark on QuAC](III.%20Benchmark%20on%20QuAC): QuAC Benchmark dataset and evaluation Script for LLM Model
   - [Data](III.%20Benchmark%20on%20QuAC/Data) : Dataset for the Benchmark 
   - [Result](III.%20Benchmark%20on%20QuAC/Result) : Evaluation result 
   - [Scripts](III.%20Benchmark%20on%20QuAC/Scripts) : Evaluation Scripts 
- [IV. Benchmark on SqUAD](IV.%20Benchmark%20on%20SqUAD): SqUAD Benchmark dataset and evaluation Script for LLM Model
   - [Data](IV.%20Benchmark%20on%20SqUAD/Data) : Dataset for the Benchmark 
   - [Result](IV.%20Benchmark%20on%20SqUAD/Result) : Evaluation result 
   - [Scripts](IV.%20Benchmark%20on%20SqUAD/Scripts) : Evaluation Scripts 
- [V. Benchmark on CoQA](V.%20Benchmark%20on%20CoQA): CoQA Benchmark dataset and evaluation Script for LLM Model
   - [Data](V.%20Benchmark%20on%20CoQA/Data) : Dataset for the Benchmark 
   - [Result](V.%20Benchmark%20on%20CoQA/Result) : Evaluation result 
   - [Scripts](V.%20Benchmark%20on%20CoQA/Scripts) : Evaluation Scripts 
- [VI. Benchmark on TydiQA](VI.%20Benchmark%20on%20TydiQA): TydiQA Benchmark dataset and evaluation Script for LLM Model
   - [Data](VI.%20Benchmark%20on%20TydiQA/Data) : Dataset for the Benchmark 
   - [Result](VI.%20Benchmark%20on%20TydiQA/Result) : Evaluation result 
   - [Scripts](VI.%20Benchmark%20on%20TydiQA/Scripts) : Evaluation Scripts 
- [VII. Benchmark on Dolly](VII.%20Benchmark%20on%20Dolly): Dolly Benchmark dataset and evaluation Script for LLM Model
   - [Data](Data) : Dataset for the Benchmark 
   - [Result](Result) : Evaluation result 
   - [Scripts](Scripts) : Evaluation Scripts 
