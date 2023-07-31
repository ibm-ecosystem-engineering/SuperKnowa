# RLHF - Reinforcement Learning using Human Feedback 
This repo contains notebook to train a reward model and then finetune the LLM using Reinforcement Learning. 

![RLHF](./Screenshots/Screenshot%202023-07-21%20at%209.27.53%20AM.png)

## Notebook :
1. [rewardModelTraining.ipynb](../7.%20Feedback%20%26%20Reward%20Model/notebooks/rewardModelTraining.ipynb) : This notebook takes in user preference data as input and trains a model of choice to output scaler reward.
2. [RLHFImplementation.ipynb](../7.%20Feedback%20%26%20Reward%20Model/notebooks/RLHFImplementation.ipynb) : This notebook takes a SFT LLM, a reward model and data as input. It then finetunes the LLM using PPO.

## Output :
The trained model gets saved in this folder

## Input :
The input dataset is placed here, which can be used to train SFT LLM and reward model.

To find a detailed overview of Reward Modeling and RLHF, refer to the medium blog:
- blog1.com
- blog2.com

## References :

1. https://github.com/lvwerra/trl
2. https://argilla.io/blog/argilla-for-llms/
