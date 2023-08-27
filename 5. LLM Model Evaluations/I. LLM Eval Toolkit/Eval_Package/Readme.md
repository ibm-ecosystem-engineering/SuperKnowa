## Evaluation Package 


## Step 1

### Install dependencies
Run `pip3 install -r setup.txt` 

#### Setup the bleurt package
```pip install --upgrade pip  # ensures that pip is current
git clone https://github.com/google-research/bleurt.git
cd bleurt
pip install .
cd ..
```

## Step 2

### Setting Up JSON Configuration for Model Evaluation

#### JSON Configuration
The JSON configuration consists of three main sections: model, data, and result.

1. Model Configuration
In the model section, you need to provide your API key and specify the model name.

```
{
  "model": {
    "watsonxai_token": "Bearer Your-API-Key",
    "model_name": "google/flan-t5-xxl"
  },
  ...
}
```
Replace Your-API-Key with your actual API key.


2. Data Configuration

The data section contains parameters related to the input data and evaluation.

```
{
  ...
  "data": {
    "data_path": "path/to/dataset",
    "question": "instruction",
    "context": "input",
    "idea_answer": "output",
    "q_num": 5
  },
  ...
}
```

- <b>data_path</b>: Provide the path to the dataset file (Ex CoQA.json).
- <b>question</b>: Specify the column or field name in the dataset that contains the questions.
- <b>context</b>: Specify the column or field name in the dataset that contains the context or input information.
- <b>idea_answer</b>: Specify the column or field name in the dataset that contains the ideal answers for evaluation.
- <b>q_num</b>: Specify the number of questions to be evaluated from the dataset.


3. Result Configuration

The result section is used to define the file where the evaluation results will be saved.

```
{
  ...
  "result": {
    "result_file": "path/to/result-file.csv"
  }
}
```

- <b>result_file</b>: Provide the path to the CSV file where the evaluation results will be stored.

### Naming convention :
modelname_sourcedata_retriever_reranker_evaluatedOn.csv

Examples :
flan-t5-xxl_excludeRedbooks_ES_colBERT_IBMTest.csv
flan-t5-xxl_passageAvailable_NA_NA_QuAC.csv

## Step 3

Run the evaluation script

`python eval_script.py`

Evaluation 
Run the evaluation result will be generated into a provided path for `result_file`.  
#### Make your result path connected with MLFlow results. 


