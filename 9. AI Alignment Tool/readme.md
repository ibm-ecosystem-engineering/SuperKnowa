# AI Alignment Tool

**Code Coming Soon**

The focus of this subdirectory is the SuperKnowa mechanism for collecting human feedback. Collecting input from users can play a crucial role in assessing a model’s response and enhancing its performance and implementing for a Retrieval-Augmented Generation (RAG) pipeline.

We focus on fine-grained human feedback on the basis of the following criteria:

- Does the generated output display lack of relevance, repetition, and inconsistency?
- Does the generated output contain inaccurate or unverifiable information?
- Does the generated output include all relevant information? Partial information?

We gather feedback through various mechanisms.

- **Ratings:** Rating feedback involves assigning a numerical value to a model's response based on its perceived quality or relevance. For instance, a user might rate a generated response on a scale of 1 to 5, indicating their satisfaction with the answer. It is quick and quantifiable, suitable for assessing overall quality.
- **Questionnaires:** Yes/no questionnaires present users with specific questions about the response. Targeted feedback on specific aspects, such as relevance to the topic. It can help to gather focused feedback on the accuracy of the response.
- **Comments:** Comment-based feedback lets users provide textual explanations for their preferences or suggestions for improvement. These comments offer valuable insights into the strengths and weaknesses of model responses.

## Reference Architecture

![superknowa](https://github.com/EnterpriseLLM/SuperKnowa/assets/111310676/278bced3-9253-4cf7-9b2f-0690b72a9f0b)

## Workflow

### User poses a question

![image](https://github.com/ibm-ecosystem-engineering/SuperKnowa/assets/111310676/5db727f1-8a50-427f-89ed-458bb3a98252)

### The system returns an answer 

The user has the ability to rate the answer that was returned. 

![image](https://github.com/ibm-ecosystem-engineering/SuperKnowa/assets/111310676/cabbfc7d-74af-4ec0-8dd7-2a6dea3a4984)

### Collecting feedback




