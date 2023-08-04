from sentence_transformers import SentenceTransformer, util
model1 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
from transformers import BertTokenizer, BertModel
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model2 = BertModel.from_pretrained("bert-base-uncased")

import math
import os
import time
from textwrap import dedent
from PIL import Image
import json
import re
import pandas as pd
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from nltk.translate import meteor_score as ms
from rouge_score import rouge_scorer
from bs4 import BeautifulSoup
import requests
import nltk
import gc
import torch
from nltk.translate import bleu_score
import numpy as np
from simhash import Simhash
from bleurt import score
import string
import collections
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

nltk.download('punkt')
nltk.download('wordnet')

# Load the configuration from the JSON file
with open('config.json', 'r') as json_file:
    config_data = json.load(json_file)

# Get the model details from the 'model' section
bam_token = config_data['model']['watsonxai_token']
model_name = config_data['model']['model_name']

# Get the data details from the 'data' section
data_path = config_data['data']['data_path']
question_column = config_data['data']['question']
idea_answer_column = config_data['data']['idea_answer']
context_column = config_data['data']['context']
q_num = config_data['data']['q_num']

# Get the result details from the 'result' section
result_file = config_data['result']['result_file']



def normalize_answer(s):

    def remove_articles(text):
        regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
        return re.sub(regex, ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def bert_score(reference, candidate, return_similarity_matrix=False):
    # Load the BERT tokenizer and model
    # Tokenize the input text
    ref_tokens = tokenizer(reference, return_tensors="pt", add_special_tokens=False)
    can_tokens = tokenizer(candidate, return_tensors="pt", add_special_tokens=False)
    # Get the BERT embeddings
    model2.eval()
    with torch.no_grad():
        ref_outputs = model2(**ref_tokens)
        ref_embeddings = ref_outputs.last_hidden_state[0]
        can_outputs = model2(**can_tokens)
        can_embeddings = can_outputs.last_hidden_state[0]
    # Compute cosine similarities
    cosine_similarities = np.zeros((can_embeddings.shape[0], ref_embeddings.shape[0]))
    for i, c in enumerate(can_embeddings):
        for j, r in enumerate(ref_embeddings):
            cosine_similarities[i, j] = cosine_similarity(c, r)
    # Align cosine similarities
    max_similarities = cosine_similarities.max(axis=1)
    # Average similarity scores
    bertscore = max_similarities.mean()
    if return_similarity_matrix:
        return bertscore, cosine_similarities
    else:
        return bertscore



def sentence_similarity(ideal_answer, generated_answer):
    #Compute embedding for both lists
    embedding_1= model1.encode(ideal_answer, convert_to_tensor=True)
    embedding_2 = model1.encode(generated_answer, convert_to_tensor=True)
    sim_score = util.pytorch_cos_sim(embedding_1, embedding_2)
    sim_score = sim_score.numpy()[0][0]
    return sim_score

def normalize_answer(s):
  """Lower text and remove punctuation, articles and extra whitespace."""
  def remove_articles(text):
    regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
    return re.sub(regex, ' ', text)
  def white_space_fix(text):
    return ' '.join(text.split())
  def remove_punc(text):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in text if ch not in exclude)
  def lower(text):
    return text.lower()
  return white_space_fix(remove_articles(remove_punc(lower(s))))

def get_tokens(s):
  if not s: return []
  return normalize_answer(s).split()

def compute_f1(a_gold, a_pred):
      gold_toks = get_tokens(a_gold)
      pred_toks = get_tokens(a_pred)
      common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
      num_same = sum(common.values())
      if len(gold_toks) == 0 or len(pred_toks) == 0:
        # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
        return int(gold_toks == pred_toks)
      if num_same == 0:
        return 0
      precision = 1.0 * num_same / len(pred_toks)
      recall = 1.0 * num_same / len(gold_toks)
      f1 = (2 * precision * recall) / (precision + recall)
      return f1

def Sim_hash(ideal_answer,generated_answer):
    return Simhash(generated_answer).distance(Simhash(ideal_answer))

def calculate_perplexity(ideal_answer,answer):
    answer_tokens = answer.strip().split()
    ideal_tokens = ideal_answer.strip().split()

    # Build a frequency distribution of ideal tokens
    token_frequency = {}
    total_tokens = 0
    for token in ideal_tokens:
        token_frequency[token] = token_frequency.get(token, 0) + 1
        total_tokens += 1

    # Calculate perplexity
    log_sum = 0
    for token in answer_tokens:
        frequency = token_frequency.get(token, 0)
        if frequency == 0:
            # Set a small probability for unseen tokens
            probability = 1 / (total_tokens + 1)
        else:
            probability = frequency / total_tokens
        log_sum += math.log2(probability)
    if len(answer_tokens) > 0:
        perplexity = 2 ** (-log_sum / len(answer_tokens))
    else:
        perplexity = 0
    return perplexity

def bleurt_score(ideal_answer,generated_answer):

    checkpoint = "bleurt/bleurt/test_checkpoint"
    scorer = score.BleurtScorer(checkpoint)
    scores = scorer.score(references=[generated_answer], candidates=[ideal_answer])
    assert isinstance(scores, list) and len(scores) == 1
    return scores[0]

def blue(answer, ideal_answer):
    # Tokenize the generated and reference answers
    generated_tokens = nltk.word_tokenize(answer)
    reference_token_lists = [nltk.word_tokenize(answer) for answer in [ideal_answer]]
    # Calculate the BLEU score
    bleu_score =  nltk.translate.bleu_score.sentence_bleu(reference_token_lists, generated_tokens)

    # bert_score_1=bert_score(ideal_answer, answer)
    # sentence_similarity_1=sentence_similarity(ideal_answer, answer)
    # Sim_hash_1=Sim_hash(ideal_answer, answer)
    # calculate_perplexity_1=calculate_perplexity(ideal_answer, answer)
    # bleurt_score_1=bleurt_score(ideal_answer, answer)
    # compute_f1_1=compute_f1(ideal_answer, answer)
    return bleu_score#, meteor_score, rouge_score#, bert_score_1,sentence_similarity_1,Sim_hash_1,calculate_perplexity_1,bleurt_score_1,compute_f1_1

def meteor(answer, ideal_answer):

    generated_tokens = nltk.word_tokenize(answer)
    reference_token_lists = [nltk.word_tokenize(answer) for answer in [ideal_answer]]
    # Calculate the METEOR score
    meteor_score = ms.meteor_score(reference_token_lists, generated_tokens)
    # Instantiate a ROUGE scorer
    return meteor_score

def rouge(answer, ideal_answer):

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    # Calculate the ROUGE score
    score = scorer.score(answer, ideal_answer)
    # Extract the F1 score for ROUGE-1
    rouge_score = score['rouge1'].fmeasure
    return rouge_score



def evaluation_script(q_num,watsonxai_token, model_name, data_path, question_column, idea_answer_column, context_column, result_file):
    
    print("Watsonxai Token:", watsonxai_token)
    print("Model Name:", model_name)
    print("Data Path:", data_path)
    print("Question Column:", question_column)
    print("Idea Answer Column:", idea_answer_column)
    print("Context Column:", context_column)
    print("Result File:", result_file)



    chat_history = ""


    # Get the file extension
    file_extension = os.path.splitext(data_path)[1].lower()

    # Load data based on file extension
    if file_extension == ".json":
        df = pd.read_json(data_path)
    elif file_extension in [".csv", ".txt"]:
        df = pd.read_csv(data_path)
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(data_path)
    else:
        print("Error: The file format is not supported.")

    df=df[0:5]

    ans = []
    qs=[]
    ians=[]

    count=0
    max_retries = 3 
    for i in range(len(df[question_column])):

        context = df[context_column][i]
        question = df[question_column][i]
        ideal_answer = df[idea_answer_column][i]

        retries = 0
        while retries < max_retries and count <= 1000:
            try:

                print("---------- question",question)
                print("---------- question no:",count)

                chat_history = f"Answer the question based on the context below. " + \
                    "Context: "  + context + \
                    " Question: " + question

                model_input = chat_history.replace("<split>", "\n")
                print("INPUT PROMPT: ", model_input)
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': watsonxai_token,
                }
                
                json_data = {

                    'model_id': model_name,
                    'inputs':  [model_input],
                     
                        #Coga
                        "parameters": {
                          "decoding_method": "greedy",
                          "temperature": 0.7,
                          "top_p": 1,
                          "top_k": 50,
                          "min_new_tokens": 10,
                          "max_new_tokens": 200
                    },
                }
                
                #watsonxai
                response = requests.post('https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29', headers=headers, json=json_data)


                json_response = json.loads(response.content.decode("utf-8"))
                print("watsonxai OUTPUT: ", json_response)

                model_output1 = json_response['results'][0]['generated_text']
                model_output1 = model_output1.replace("Question", '')
                model_output1 = model_output1.replace("Answer: ", '')
                model_output1 = re.sub(r'\[[^\]]*\]|\.', '',model_output1)

                # Seprate sentences
                sentences = model_output1.split(". ")
                # remove duplicates SENTENCES
                unique_sentences = list( dict.fromkeys(sentences))

                if not model_output1.endswith("."):
                # remove the last sentence if not . at last
                    unique_sentences.pop()

                # join unique sentences back into a text 
                model_output = ". ".join(unique_sentences)+ "."
                
                print("FINAL ANSWER: ", model_output1) 

                ans.append(model_output1)
                qs.append(question)
                ians.append(ideal_answer)


                gc.collect()
                torch.cuda.empty_cache()
                count+=1
                break

            except Exception as e:
                print(f"Question failed: {question}")
                retries += 1
                if retries >= max_retries:
                    print(f"Question failed after {max_retries} attempts. Moving on to the next question.")
                    ans.append("")
                    break  # Break the retry loop and move to the next question
                else:
                    print(f"Retrying question. Attempt {retries + 1} of {max_retries}.")
                    time.sleep(2)

    df = pd.DataFrame()
    df["question"]=qs
    df["answer"]=ans
    df["ideal_answer"]=ians


    df["blue score"] = df.apply(lambda x: blue(str(x.ideal_answer), str(x.answer)), axis=1)
    df['meteor score'] = df.apply(lambda x: meteor(str(x.ideal_answer), str(x.answer)), axis=1)
    df['rouge score'] = df.apply(lambda x: rouge(str(x.ideal_answer), str(x.answer)), axis=1)
    df['SentenceSim score'] = df.apply(lambda x: sentence_similarity(str(x.ideal_answer), str(x.answer)), axis=1)
    df['SimHash score'] = df.apply(lambda x: Sim_hash(str(x.ideal_answer), str(x.answer)), axis=1)
    # df['MMR score'] = df.apply(lambda x: calculate_mrr(x.ideal_answer, [x.answer]), axis=1)
    df['perplexity score'] = df.apply(lambda x: calculate_perplexity(str(x.ideal_answer), str(x.answer)), axis=1)
    df['bleurt score'] = df.apply(lambda x: bleurt_score(str(x.ideal_answer), str(x.answer)), axis=1)
    df['F1 score'] = df.apply(lambda x: compute_f1(normalize_answer(str(x.ideal_answer)), normalize_answer(str(x.answer))), axis=1)
    try:
        df["bert score"] = df.apply(lambda x: bert_score(str(x.ideal_answer), str(x.answer)), axis=1)
    except Exception as e:
        print(f"Error calculating BERT score: {e}")

    df.to_csv(result_file, index=False)


evaluation_script(q_num, bam_token, model_name, data_path, question_column, idea_answer_column, context_column, result_file)
