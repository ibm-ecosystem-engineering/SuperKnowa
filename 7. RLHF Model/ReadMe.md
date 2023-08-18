# RLHF - Reinforcement Learning using Human Feedback 

This directory contains notebooks that can be used to train a reward model, and then fine-tune the LLM using Reinforcement Learning. For a detailed overview of Reward Modeling and RLHF, refer to:

- [RLHF Reward Model Training](https://medium.com/towards-generative-ai/reward-model-training-2209d1befb5f)
- [Measuring AI Alignment using Human Feedback for RAG Architecture](https://medium.com/towards-generative-ai/human-feedback-evaluation-for-rag-pipeline-93e008c69890)

## Architecture

![RLHF](./Screenshots/Screenshot%202023-07-21%20at%209.27.53%20AM.png)

## Notebooks

1. [rewardModelTraining.ipynb](../7.%20Feedback%20%26%20Reward%20Model/notebooks/rewardModelTraining.ipynb) : This notebook takes in user preference data as input and trains a model of choice to output scaler reward.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXBjaTc5cWJzbnBnaXZydTYyYnlqcHpxMDFpdmNyejZudTNidjFsYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3PyP8FDINh3MZji2Cw/giphy.gif" alt="GIF Description" width="500" height="300">

2. [RLHFImplementation.ipynb](../7.%20Feedback%20%26%20Reward%20Model/notebooks/RLHFImplementation.ipynb) : This notebook takes a SFT LLM, a reward model and data as input. It then finetunes the LLM using PPO.

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa21kdHFnbzhocG10ZGozZnUycnYxYWhtbzFtc2FmeWRpdGkweXh6cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Hxpvnqe4pZ0L7G12OX/giphy.gif" alt="GIF Description" width="500" height="300">

## References 

1. https://github.com/lvwerra/trl
2. https://argilla.io/blog/argilla-for-llms/
