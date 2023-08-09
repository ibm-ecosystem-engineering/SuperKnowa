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

import sys
from typing import List
from peft import PeftModel
 
import fire
import torch
from peft import PeftModel
import transformers
import gradio as gr

from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


bamToken = os.getenv('BAM_TOKEN')

#os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb=0'
print("--- bam key", bamToken)


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

    perplexity = 2 ** (-log_sum / len(answer_tokens))
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
df=df[0:10]

print("----- length",len(df.question))
ans = []


quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload=True)
 
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"




load_8bit: bool = False,
base_model: str = "decapoda-research/llama-7b-hf",
lora_weights: str = "/root/finetune/experiments",

    

tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf")
model = LlamaForCausalLM.from_pretrained(
    "decapoda-research/llama-7b-hf",
    #load_in_8bit=True,
    #torch_dtype=torch.float16,
    device_map="auto",
    #device_map=device_map,
    quantization_config=quantization_config,
    )

# model = PeftModel.from_pretrained(
#             model,
#             "/root/finetune/experiments",
#             device_map={"": DEVICE},
#             torch_dtype=torch.float16,
#         )

    # unwind broken decapoda-research config
model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
model.config.bos_token_id = 1
model.config.eos_token_id = 2


model.eval()
def evaluate(
        instruction,
        input=None,
        temperature=0.1,
        top_p=0.75,
        top_k=40,
        num_beams=4,
        max_new_tokens=128,
        **kwargs,
    ):
        prompt = generate_prompt(instruction, input)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(DEVICE)
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            **kwargs,
        )
        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences[0]
        print("s---",s)
        output = tokenizer.decode(s)
        print("output--",output)
        return output.split("### Response:")[1].strip()

    



def generate_prompt(instruction, input=None):
    if input:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input}

### Response:
"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:
"""

##result =evaluate("Answer the question based on the context Question: How do you use a machine learning model in jupyter notebook?","Context: Machine learning in Jupyter NotebookIll begin by going through the process of exploring the data set and building a predictive model you can use to determine the likelihood of a credit loan having risk or no risk. For this use case, the machine learning model youre building is a classification model that returns a prediction of risk (the applicants inputs on the loan application predict that there is a good chance of default on the loan) or no risk (the applicants inputs predict that the loan will be paid off). I use some fairly popular libraries and frameworks to build the model in Python using a Jupyter Notebook. After Ive built the model, I make it available for deployment so it can be used by others.")
#print("Result---",result)



max_retries = 3 
for i in range(len(df.question)):

    retries = 0
    while retries < max_retries:
        try:

            print("---------- question",df.question[i])
            print("---------- question No:",i)

            chat_history = f"Answer the question based on the context below. " + \
                "Context: "  + df.context[i] + \
                " Question: " + df.question[i]

            result = evaluate(chat_history)
            print("FINAL ANSWER: ", result)

            # chat_history += f"{model_output}<split>"
            model_output1 = f"{result}<split>"  
            
            print("FINAL ANSWER: ", model_output1)


            ans.append(model_output1)
            gc.collect()
            torch.cuda.empty_cache()
            break

        except Exception as e:
            print(f"Question failed: {df.question[i]}")
            retries += 1
            if retries >= max_retries:
                print(f"Question failed after {max_retries} attempts. Moving on to the next question.")
                ans.append("")
                break  # Break the retry loop and move to the next question
            else:
                print(f"Retrying question. Attempt {retries + 1} of {max_retries}.")
                time.sleep(2)

df["answer"] = ans



df["blue score"] = df.apply(lambda x: blue(x.ideal_answer, x.answer), axis=1)
df['meteor score'] = df.apply(lambda x: meteor(x.ideal_answer, x.answer), axis=1)
df['rouge score'] = df.apply(lambda x: rouge(x.ideal_answer, x.answer), axis=1)
df["bert score"] = df.apply(lambda x: bert_score(x.ideal_answer, x.answer), axis=1)
df['SentenceSim score'] = df.apply(lambda x: sentence_similarity(x.ideal_answer, x.answer), axis=1)
df['SimHash score'] = df.apply(lambda x: Sim_hash(x.ideal_answer, x.answer), axis=1)
# df['MMR score'] = df.apply(lambda x: calculate_mrr(x.ideal_answer, [x.answer]), axis=1)
df['perplexity score'] = df.apply(lambda x: calculate_perplexity(x.ideal_answer, x.answer), axis=1)
df['bleurt score'] = df.apply(lambda x: bleurt_score(x.ideal_answer, x.answer), axis=1)
df['F1 score'] = df.apply(lambda x: compute_f1(x.ideal_answer, x.answer), axis=1)



#new_df = pd.concat([df, scores_df], axis=1)
#new_df = new_df[new_df['answer'] != ""]
df.to_csv('SuperKnowa_CoQA_pre_Llama.csv', index=False)

print("Average BLEU score", df["blue score"].mean())
print("Average F1 score", df["F1 score"].mean())

