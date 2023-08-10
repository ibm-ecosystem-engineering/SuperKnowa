# SuperKnowa frontend Service

This particular subdirectory includes code, alongside descriptions and integration guides for the backend service, providing the creation of a frontend application.

The SuperKnowa Frontend service is intended to be used in the context of Retrieval Augmented Generation (RAG) application. It interacts with the Backend service to provide a rich user epxerience asking question and capturing feedback.

The SuperKnowa Frontend service is designed to operate within the scope of a Retrieval Augmented Generation (RAG) application. It interacts with the Backend service to deliver a rich user experience, enabling users to post questions and capture feedback effectively.

## Reference Architecture

![superknowa](https://github.com/EnterpriseLLM/SuperKnowa/assets/111310676/278bced3-9253-4cf7-9b2f-0690b72a9f0b)

## Prerequisites

SuperKnowa Frontend service relies on the Backend service. Before you start developing the Frontend service make sure you have an up and running [Backend service](https://github.com/ibm-ecosystem-engineering/SuperKnowa/tree/main/8.%20Deploy%20%26%20Infer)

## Development

### 1. Making an inference call to Backend service to get response

Backend service exposes some REST endpoints, you can get a full description of the API's in the [Backend service](https://github.com/ibm-ecosystem-engineering/SuperKnowa/tree/main/8.%20Deploy%20%26%20Infer)

In the following demonstration, I will illustrate the process of creating a user interface using ReactJS along with the Material UI framework. Feel free to select any preferred UI framework for your project.

Our initial call with the REST endpoint involves a POST request to `/api/v1/chat/<retriever>`. This request takes a question as a parameter in the request body and `<retriever>' as path parameter. Values for `retriever` is elastic or solr. Here's a sample curl command for reference:

```sh
curl --location 'http://localhost:3001/api/v1/chat/elastic' \
--header 'Content-Type: application/json' \
--data '{
    "question":"What is a watson NLP?"
}'
```

```js
axios
    .post(
      'http://localhost:3001/api/v1/chat/elastic',
      { question: question}
    )
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
```

Here is a sample react code which will make a chat window to interact with the Backend service.

```js
import {
  Box,
  OutlinedInput,
  CircularProgress,
  Button,
  useTheme,
} from "@mui/material";
import SendOutlinedIcon from "@mui/icons-material/SendOutlined";
import CancelOutlinedIcon from "@mui/icons-material/CancelOutlined";
import SyncIcon from "@mui/icons-material/Sync";
import { tokens } from "../theme";
import { useState } from "react";
import axios from "axios";
import { chatBackendURL } from "../api/config";
import { useDispatch } from "react-redux";
import { addMessages } from "../redux/displayAnswer";

let controller;

const ChatButton = (props) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const dispatch = useDispatch();

  const [lastQuestion, setLastQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    const question = props.inputRef.current.value;
    apiCall(question, false);
  };

  const handleRegenerate = () => {
    apiCall(lastQuestion, true);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleClick();
    }
  };

  const apiCall = (question, isGenerate) => {
    controller = new AbortController();

    question = question.trim();

    if (!question) return;

    setIsLoading(true); 
    setLastQuestion(question); 
    axios
      .post(
        chatBackendURL,
        { question: question, regenerate: isGenerate },
        { signal: controller.signal }
      )
      .then((response) => {
        var answer = response.data.answer;
        var source = response.data.source;
        var ref = response.data.ref;
        var model_id = response.data.model_id;

        const msg = {
          question: question,
          answer: answer,
          source: source, 
          mongoRef: ref,
          model_id: model_id
        };
        dispatch(addMessages(msg));
        setIsLoading(false);
        props.inputRef.current.value = "";
      })
      .catch((error) => {
        setIsLoading(false);

        if (error.code !== "ERR_CANCELED") {
          var errorMsg =
            "The information you are looking for is not available. Please try again later. Thank you.";
          dispatch(
            addMessages({
              question: question,
              answer: errorMsg,
              source: undefined,
              mongoRef: undefined
            })
          );
        }
      });
  };

  const handleCancelRquest = () => {
    controller.abort();
    setIsLoading(false);
  };

  return (
    <Box
      style={{
        position: "fixed",
        flexDirection: "column",
        bottom: "7vh",
        display: "flex",
        alignItems: "center",
      }}
    >
      { 
        isLoading ? (
          <Button
            variant="outlined"
            startIcon={<CancelOutlinedIcon />}
            sx={{
              border: "1px solid rgba(0,0,0,.1)",
              textTransform: "capitalize",
              bgcolor: colors.primary[400],
              color: colors.primary[200],
              margin: "10px",
              ":hover": {
                bgcolor: colors.primary[400],
                color: colors.grey[400],
                border: "1px solid rgba(0,0,0,.1)",
              },
            }}
            onClick={handleCancelRquest}
          >
            Cancel request
          </Button>
        ) : (
          <Button
            variant="outlined"
            startIcon={<SyncIcon />}
            sx={{
              border: "1px solid rgba(0,0,0,.1)",
              textTransform: "capitalize",
              bgcolor: colors.primary[400],
              color: colors.primary[200],
              margin: "10px",
              ":hover": {
                bgcolor: colors.primary[400],
                color: colors.grey[400],
                border: "1px solid rgba(0,0,0,.1)",
              },
            }}
            onClick={handleRegenerate}
          >
            Regenerate response
          </Button>
        )
      }

      <OutlinedInput
        autoFocus
        endAdornment={
          isLoading ? (
            <CircularProgress
              style={{ width: "20px", height: "24px", color: colors.grey[200] }}
            />
          ) : (
            <SendOutlinedIcon
              style={{ width: "20px", height: "24px", cursor: "pointer" }}
              onClick={handleClick}
            />
          )
        }
        placeholder="Ask something..."
        style={{
          maxHeight: "350px",
          height: "70px",
          width: "40vw",
        }}
        sx={{
          boxShadow: 12,
          backgroundColor: colors.primary[400],
        }}
        inputRef={props.inputRef}
        onKeyDown={handleKeyDown}
      />
    </Box>
  );
};

export default ChatButton;

```

The above code will create a UI like below

![image](https://github.com/ibm-ecosystem-engineering/SuperKnowa/assets/111310676/5db727f1-8a50-427f-89ed-458bb3a98252)


/api/v1/chat', methods=['POST']

/api/v1/chat/<retriever>', methods=['POST']

/api/v1/chat/multi/<retriever>/<no_model>', methods=['POST']

/api/v1/feedback/add/<mongo_ref>', methods=['PUT']

/api/v1/feedback/update/<feedback_id>', methods=['POST']

