# RLHF - Reinforcement Learning using Human Feedback 
This repo contains notebook to train a reward model and then finetune the LLM using Reinforcement Learning. 

## Notebook :
1. [rewardModelTraining.ipynb](../7.%20Feedback%20%26%20Reward%20Model/code/rewardModelTraining.ipynb) : This notebook takes in user preference data as input and trains a model of choice to output scaler reward.
2. [RLHFImplementation.ipynb](../7.%20Feedback%20%26%20Reward%20Model/code/RLHFImplementation.ipynb) : This notebook takes a SFT LLM, a reward model and data as input. It then finetunes the LLM using PPO.

## Output :
The trained model gets saved in this folder

## Input :
The input dataset is placed here, which can be used to train SFT LLM and reward model.
