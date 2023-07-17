# In-Context Learning with LLM

This directory contains a Jupyter notebook that demonstrates in-context learning using LLM. The script prompts the user for a context and a question based on that context, and then uses an LLM model to generate an answer to the question.

![In-context learning](https://production-media.paperswithcode.com/thumbnails/task/c9598674-b034-477e-b5ec-a7e324336280.jpg) 

Image Source: https://paperswithcode.com/task/question-answering

## Usage

To use the script, simply run the `process_watsonx_request` function. You will be prompted to enter a context and a question. The context should be a paragraph or two describing a situation or concept. The question should be something that can be answered based on the provided context.

Here's an example interaction:

```python
>>> process_watsonx_request()
Please enter the context: DataOps is a collaborative data management discipline that focuses on end-to-end data management and the elimination of data silos...
Please enter your question: What are the benefits of DataOps?
```

And the script will generate an answer like:

```
DataOps offers several benefits including decreasing the cycle time in deploying analytical solutions, lowering data defects, reducing the time required to resolve data defects, and minimizing data silos.
```

![Example interaction](/5.%20In-context%20learning%20using%20LLM/Screenshot/notebook.png)

## Dependencies

This script requires Python 3.6 or later, and the `requests` and `json` libraries.
