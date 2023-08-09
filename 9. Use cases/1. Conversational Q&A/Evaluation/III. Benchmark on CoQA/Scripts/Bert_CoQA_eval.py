from sentence_transformers import SentenceTransformer, util
model1 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
from transformers import BertTokenizer, BertModel
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
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
from ibm_watson import DiscoveryV2
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
from transformers import BertTokenizer, BertForQuestionAnswering
import torch


def normalize_answer(s):
    """Lower text and remove punctuation, storys and extra whitespace."""

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

    

def bert_QA(question, context):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModelForQuestionAnswering.from_pretrained("bert-base-uncased")

    # Tokenize the question and context
    inputs = tokenizer.encode_plus(question, context, return_tensors='pt', add_special_tokens=True)

    # Get the tokenized input IDs, attention mask, and token type IDs
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    token_type_ids = inputs['token_type_ids']

    # Perform the question answering inference
    outputs = model(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)

    # Get the start and end logits from the model outputs
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    # Find the most probable answer span
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits)

    # Convert the token indices to actual tokens in the context
    answer_tokens = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][start_index:end_index+1]))

    # Return the answer
    return answer_tokens


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
    if len(answer_tokens) >0:
        perplexity = 2 ** (-log_sum / len(answer_tokens))
    else:
        perplexity=0
    return perplexity

def bleurt_score(ideal_answer,generated_answer):

    checkpoint = "/Users/sahil/Documents/bleurt/bleurt/test_checkpoint"
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

# def calculate_mrr(ideal_answers,predictions):
#     total_reciprocal_rank = 0
#     num_questions = len(predictions)

#     for i in range(num_questions):
#         predicted_answers = predictions[i]
#         ideal_answer = ideal_answers[i]

#         reciprocal_rank = 0

#         for rank, answer in enumerate(predicted_answers, 1):
#             if answer == ideal_answer:
#                 reciprocal_rank = 1 / rank
#                 break

#         total_reciprocal_rank += reciprocal_rank

#     mrr = total_reciprocal_rank / num_questions
#     return mrr


chat_history = ""

df = pd.read_json("alpaca_data.json")
df.columns = ["question","context","ideal_answer"]
df=df[df.context != ""].reset_index().drop("index",axis=1)
df=df[0:1000]

print("----- length",len(df.question))
ans = []

max_retries = 3 
for i in range(len(df.question)):

        # retries = 0
        # while retries < max_retries:
        #     try:

                print("---------- question",df.question[i])
                print("---------- question No:",i)

                answer = bert_QA(df.question[i], df.context[i])

                print("Context -- ",df.context[i])
                
                print("FINAL ANSWER: ", answer)
   

                ans.append(answer)
                gc.collect()
                torch.cuda.empty_cache()
            #     break

            # except Exception as e:
            #     print(f"Question failed: {df.question[i]}")
            #     retries += 1
            #     if retries >= max_retries:
            #         print(f"Question failed after {max_retries} attempts. Moving on to the next question.")
            #         ans.append("")
            #         break  # Break the retry loop and move to the next question
            #     else:
            #         print(f"Retrying question. Attempt {retries + 1} of {max_retries}.")
            #         time.sleep(2)

df["answer"] = ans


#scores_df = df.apply(lambda row: pd.Series(calculate_scores(model_output1, row["ideal_answer"])), axis=1)

#print(scores_df)
#scores_df.columns = ["BLEU score", "METEOR score", "ROUGE score"]
# scores_df.columns = ["BLEU score", "METEOR score", "ROUGE score","bert score","sentence similarity","Sim hash","calculate perplexity","bleurt score","F1 score"]


df.to_csv('Bert_CoQA_answer.csv', index=False)

df["blue score"] = df.apply(lambda x: blue(x.ideal_answer, x.answer), axis=1)
df['meteor score'] = df.apply(lambda x: meteor(x.ideal_answer, x.answer), axis=1)
df['rouge score'] = df.apply(lambda x: rouge(x.ideal_answer, x.answer), axis=1)
df['SentenceSim score'] = df.apply(lambda x: sentence_similarity(x.ideal_answer, x.answer), axis=1)
df['SimHash score'] = df.apply(lambda x: Sim_hash(x.ideal_answer, x.answer), axis=1)
# df['MMR score'] = df.apply(lambda x: calculate_mrr(x.ideal_answer, [x.answer]), axis=1)
df['perplexity score'] = df.apply(lambda x: calculate_perplexity(x.ideal_answer, x.answer), axis=1)
df['bleurt score'] = df.apply(lambda x: bleurt_score(x.ideal_answer, x.answer), axis=1)
df['F1 score'] = df.apply(lambda x: compute_f1(normalize_answer(x.ideal_answer), normalize_answer(x.answer)), axis=1)
try:
    df["bert score"] = df.apply(lambda x: bert_score(x.ideal_answer, x.answer), axis=1)
except Exception as e:
    print(f"Error calculating BERT score: {e}")


#new_df = pd.concat([df, scores_df], axis=1)
#new_df = new_df[new_df['answer'] != ""]
df.to_csv('BertBase_CoQA_Eval_result.csv', index=False)


