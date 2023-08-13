# SuperKnowa frontend Service

This particular subdirectory includes code, alongside descriptions and integration guides for the backend service, providing the creation of a frontend application.

The SuperKnowa Frontend service is designed to operate within the scope of a Retrieval Augmented Generation (RAG) application. It interacts with the Backend service to deliver a rich user experience, enabling users to post questions and capture feedback effectively.

## Reference Architecture

![superknowa](https://github.com/EnterpriseLLM/SuperKnowa/assets/111310676/278bced3-9253-4cf7-9b2f-0690b72a9f0b)

## Prerequisites

SuperKnowa Frontend service relies on the Backend service. Before you start developing the Frontend service make sure you have an up and running [Backend service](https://github.com/ibm-ecosystem-engineering/SuperKnowa/tree/main/8.%20Deploy%20%26%20Infer)

## Development

### 1. Making an inference call to Backend service to get response

Backend service exposes some REST endpoints, you can get a full description of the API's in the [Backend service](https://github.com/ibm-ecosystem-engineering/SuperKnowa/tree/main/8.%20Deploy%20%26%20Infer)



![image](https://github.com/ibm-ecosystem-engineering/SuperKnowa/assets/111310676/5db727f1-8a50-427f-89ed-458bb3a98252)

### 2. Display response by the Backend service



![image](https://github.com/ibm-ecosystem-engineering/SuperKnowa/assets/111310676/cabbfc7d-74af-4ec0-8dd7-2a6dea3a4984)

### 1. Collecting feedback

To implement the feedback mechanism, we focused on fine-grained human feedback on the basis of the following criteria,

- Output influenced by lack of relevance, repetition, and inconsistency.
- Generated output containing inaccurate or unverifiable information.
- Generated response is missing or partial information.

We gather feedback through various methods.

- Rating
- Q&A Questionnaires
- Feedback/comments

**Rating:** Rating feedback involves assigning a numerical value to a model's response based on its perceived quality or relevance. For instance, a user might rate a generated response on a scale of 1 to 5, indicating their satisfaction with the answer. It is quick and quantifiable, suitable for assessing overall quality.

**Q&A Questionnaires:** Yes/no questionnaires present users with specific questions about the response. Targeted feedback on specific aspects, such as relevance to the topic. It can help to gather focused feedback on the accuracy of the response.

**Comments:** Comment-based feedback lets users provide textual explanations for their preferences or suggestions for improvement. These comments offer valuable insights into the strengths and weaknesses of model responses.


