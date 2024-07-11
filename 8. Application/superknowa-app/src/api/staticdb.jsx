
const examples_solr_b = [
    "What is watson knowledge catalog?",
    "What is the difference between OpenShift and Kubernetes?",
    "Can Instana use OpenTelemetry trace data?",
    "What is Watson NLP library?",
    "Which IBM product can be used for transforming data?",
];

const examples_solr = [
    "What is watson knowledge catalog?",
    "What is the difference between OpenShift and Kubernetes?",
    "Can Instana use OpenTelemetry trace data?",
    "What is Watson NLP library?",
    "Which IBM product can be used for transforming data?",
];

const examples = [
    "What is watson knowledge catalog?",
    "What is the difference between OpenShift and Kubernetes?",
    "Can Instana use OpenTelemetry trace data?",
    "What is Watson NLP library?",
    "Which type of models can be built by AutoAI?",
];


const suggestions = [
    "Please add '?' At the end of your questions​",
    "The data has been scraped from IBM Developer, IBM documentation and Medium Blogs. It should not hallucinate. In case you notice anything, please let us know.",
    "Try adding context after the question like \"Summarize / Explain\" etc. For better results.​",
    "We have not scaled this for use. Also sometimes responses maybe delayed due to traffic on server. Be patient."

];

const limitations = [
    "Answers could be sometimes repeated or truncated. We are working on it.​",
    "Currently No prompt-tuning or fine-tuning in place, so some prompts may not work.​",
    "No re-ranking in place for relevancy (of official pages) or recency of the answer. So some answers may be dated.",
    "Currently no human feedback loop implemented. We are working on it. ​"
];

const appLabels = {
    app_version: "Beta version",
    offline_version: "Offline version",
    multi_version: "Multi-model version",
    page_heading: "IBM SuperKnowa",
    page_sub_heading: "Ask me anything about any IBM product",
    page_org_name: "Ecosystem Engineering",
    page_header_multi: "Multi model",
    dmenu_drawer_title: "SuperKnowa",
    dmenu_home: "Home",
    dmenu_custom_context: "Add your pdf file",
    dmenu_multimodel: "Multi model",
}

export {examples, suggestions, limitations, appLabels};