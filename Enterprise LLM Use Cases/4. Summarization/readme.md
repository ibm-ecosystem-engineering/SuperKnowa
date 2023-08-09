# Text Summarization with LLM (powered by watsonx.ai)

This directory provides a solution for generating text summaries using Language Model (LLM) powered by watsonx.ai. The directory consists of Python scripts, a configuration file, a JSON payload file, and a CSS file for styling.

## Files and Descriptions

### Python Scripts

#### `summarizer.py`

This script contains the core functionality for text summarization using LLM. It includes functions or classes to load a pre-trained model, preprocess input text, generate summaries, and provide various options for customization.

#### `customApi.py`

This script contains functions or classes related to custom API integrations for the text summarization use case. It includes code to interact with specific web services, handle API requests and responses, and manage authentication and authorization.

### Configuration File

#### `app-config.properties`

This file contains key-value pairs defining various settings and parameters for the text summarization application. It includes information such as API endpoints, authentication credentials, model paths, and other customizable options.

### JSON Payload File

#### `summary-payload.json`

This JSON file defines a payload for interacting with a summarization service or API. It can include the text to be summarized, specific parameters for summarization, and other relevant information.

### CSS File

#### `customStyles.css`

This CSS file contains custom styling rules and definitions that can be used to enhance the visual appearance of the web interface or any HTML-based output related to the summarization project.

## Usage

### 1. Set Up the Environment

Ensure that you have the necessary dependencies installed and configure the settings in `app-config.properties` as needed.

### 2. Run the Summarizer

Use the `summarizer.py` script to create a dash app for generating summaries for your input text. Follow the instructions in the script for customization and usage.

### 3. Utilize the Custom API

If needed, use the `customApi.py` script to interact with specific web services or APIs for summarization.

### 4. Apply Custom Styling

Use the `customStyles.css` file to apply custom styling to the web interface or HTML output, as needed.

### 5. Customize and Extend

Feel free to modify the code, experiment with different summarization techniques, and extend the functionality to suit your specific needs and use cases.
