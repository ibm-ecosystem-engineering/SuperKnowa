# SuperKnowa Benchmark evaluation

This directory contains LLM Model Evaluation scripts and Benchmark data for evaluating SuperKnowa RAG pipeline. 

   - [I. Benchmark on QuAC](III.%20Benchmark%20on%20QuAC): QuAC Benchmark dataset and evaluation Script for LLM Model
      - [Data](III.%20Benchmark%20on%20QuAC/Data) : Dataset for the Benchmark 
      - [Result](III.%20Benchmark%20on%20QuAC/Result) : Evaluation result 
      - [Scripts](III.%20Benchmark%20on%20QuAC/Scripts) : Evaluation Scripts 
   - [II. Benchmark on SqUAD](IV.%20Benchmark%20on%20SqUAD): SqUAD Benchmark dataset and evaluation Script for LLM Model
      - [Data](IV.%20Benchmark%20on%20SqUAD/Data) : Dataset for the Benchmark 
      - [Result](IV.%20Benchmark%20on%20SqUAD/Result) : Evaluation result 
      - [Scripts](IV.%20Benchmark%20on%20SqUAD/Scripts) : Evaluation Scripts 
   - [III. Benchmark on CoQA](V.%20Benchmark%20on%20CoQA): CoQA Benchmark dataset and evaluation Script for LLM Model
      - [Data](V.%20Benchmark%20on%20CoQA/Data) : Dataset for the Benchmark 
      - [Result](V.%20Benchmark%20on%20CoQA/Result) : Evaluation result 
      - [Scripts](V.%20Benchmark%20on%20CoQA/Scripts) : Evaluation Scripts 
   - [IV. Benchmark on TydiQA](VI.%20Benchmark%20on%20TydiQA): TydiQA Benchmark dataset and evaluation Script for LLM Model
      - [Data](VI.%20Benchmark%20on%20TydiQA/Data) : Dataset for the Benchmark 
      - [Result](VI.%20Benchmark%20on%20TydiQA/Result) : Evaluation result 
      - [Scripts](VI.%20Benchmark%20on%20TydiQA/Scripts) : Evaluation Scripts 

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
