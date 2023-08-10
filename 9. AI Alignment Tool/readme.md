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

### 2. Display response by the Backend service

To present the message received from the backend service, you can structure your component as shown in the following design:

```js
import { Box, Grid, useTheme, Button, Link } from "@mui/material";
import { useState } from "react";
import { tokens } from "../theme";
import AnswerFeedbackDialog from "./AnswerFeedbackDialog";
import CommentIcon from "@mui/icons-material/Comment";
import Tooltip from "@mui/material/Tooltip";
import AnswerRating from "./AnswerRating";

const Answer = (
    { 
      answer, 
      question,
      source, 
      mongoRef, 
      model_id,
      type
    }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [open, setOpen] = useState(false);
  const [feedbackReference, setFeedbackReference] = useState(null); 


  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Grid
      container
      spacing={1}
      borderRadius={"5px"}
      mt={"5px"}
      p={"10px"}
      borderColor={colors.primary[400]}
      sx={{
        backgroundColor: colors.primary[400],
      }}
    >
      <Grid item xs={10} minHeight={'140px'}>
        <span>{answer}</span>
        <Box
          display={"flex"}
          flexDirection={"row"}
          alignContent={"space-between"}
        >
          <Box display={"flex"} flexGrow={1}>
            {source && source != "None" && (
              <div style={{ fontStyle: "italic" }}>
                Reference:{" "}
                <Link href={source} target="_blank" variant="a" color="inherit">
                  link
                </Link>
              </div>
            )}
          </Box>
          <AnswerFeedbackDialog
            open={open}
            handleClose={handleClose}
            answer={answer}
            title={""}
            mongoRef={mongoRef}
            question={question}
            feedbackReference={feedbackReference}
            setFeedbackReference={setFeedbackReference}
            model_id={model_id}
          />
        </Box>
      </Grid>
      <Grid item xs={2}>
        <Box height={'100%'} display={'flex'} justifyContent={'space-between'} flexDirection={'column'}>
          <AnswerRating 
            handleClickOpen={handleClickOpen} 
            model_id={model_id}
            answer={answer}
            mongoRef={mongoRef}
            question={question}
            feedbackReference={feedbackReference}
            setFeedbackReference={setFeedbackReference}
            type={type}
          />
          <Tooltip title="Add additional feedback">
            <Button
              onClick={handleClickOpen}
              endIcon={<CommentIcon />}
              sx={{ color: colors.grey[300] }}
            ></Button>
          </Tooltip>
          </Box>
      </Grid>
    </Grid>
  );
};

export default Answer;
```

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

Here is the implementation designing with reactJS and materialUI.

**Rating component:**

```js
import { Box, Grid, useTheme, Rating } from "@mui/material";
import { useState } from "react";
import StarIcon from "@mui/icons-material/Star";
import { saveRating } from "../api/feedback/feedback_api";

const labels = {
    1: "Gibberish/Incorrect/Wrong",
    2: "Partially correct",
    3: "Correct but incomplete/truncated sentence",
    4: "Correct but Repetitive phrases/sentences",
    5: "Excellent",
};

function getLabelText(value) {
  return `${value} Star${value !== 1 ? 's' : ''}, ${labels[value]}`;
}

const AnswerRating = ({
  handleClickOpen,
  model_id,
  answer,
  question,
  mongoRef,
  feedbackReference,
  setFeedbackReference,
  type
}) => {
   const [value, setValue] = useState(-1);
   const [hover, setHover] = useState(-1);

   const handleFeedback = (feedback) => {
      setValue(feedback);

      let rating = {
        "feedbackDate": new Date().toISOString(),
        "question": question,
        "rating": [{
          "star": feedback,
          "model_id": model_id,
        }],
        "answers": [{
          "answer": answer,
          "model_id": model_id,
        }],
        "type": type
      }
      saveRating(rating,mongoRef,feedbackReference,setFeedbackReference);

      if(feedback < 2)
        handleClickOpen()
  };

  return (
    <>
      <Rating
        name="hover-feedback"
        value={value}
        precision={1}
        getLabelText={getLabelText}
        onChange={(event, newValue) => {
          handleFeedback(newValue);
        }}
        onChangeActive={(event, newHover) => {
          setHover(newHover);
        }}
        emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
      />
      {value !== null && (
        <Box sx={{ ml: 3 }}>{labels[hover !== -1 ? hover : value]}</Box>
      )}
    </>
  );
};

export default AnswerRating;
```
**Q&A and Comments component**

```js
import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import { useState } from "react";
import { tokens } from "../theme";
import { useTheme } from "@mui/material";
import ThumbUpOutlinedIcon from "@mui/icons-material/ThumbUpOutlined";
import ThumbDownOutlinedIcon from "@mui/icons-material/ThumbDownOutlined";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import TextField from "@mui/material/TextField";
import { additionalFeedback } from "../api/feedback/feedback_api";
import { Box, Grid, Typography } from "@mui/material";

const feedbackQustions = [
  "Is the response relevant and coherent?",
  "Was this a useful response with an appropriate amount of information?",
  "Is the response factual and accurate, based on the document?",
];

export default function AnswerFeedbackDialog({
  open,
  handleClose,
  answer,
  title,
  mongoRef,
  question,
  model_id,
  feedbackReference,
  setFeedbackReference,
  type
}) {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [formValues, setFormValues] = useState({});

  const handleSubmit = () => {
    let feedback = {
        "question": question,
        "answers": [{
          "answer": answer,
          "model_id": model_id,
        }],
        "type": type,
        "feedbackDate": new Date().toISOString(),
        "additional_feedback": [formValues]
    }
    additionalFeedback(feedback,mongoRef,feedbackReference,setFeedbackReference)
    handleClose();
  };

  return (
    <div>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Answer {title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <Typography padding={"5px"}>{answer}</Typography>
          </DialogContentText>
          <Grid container rowSpacing={1}>
            <Grid item xs={9}>
              <Typography lineHeight={"40px"}>{feedbackQustions[0]}</Typography>
            </Grid>
            <Grid item xs={3} padding={"0px"}>
              <FormControl>
                <RadioGroup
                  row
                  aria-labelledby="demo-row-radio-buttons-group-label"
                  name="row-radio-buttons-group"
                  onChange={(e) => {
                    e.preventDefault();
                    formValues.relevent = e.target.value;
                    setFormValues(formValues);
                  }}
                >
                  <FormControlLabel
                    value="yes"
                    control={
                      <Radio
                        icon={<ThumbUpOutlinedIcon color={colors.grey[300]} />}
                        checkedIcon={<ThumbUpIcon color={colors.grey[300]} />}
                        color="secondary"
                      />
                    }
                  />
                  <FormControlLabel
                    value="no"
                    control={
                      <Radio
                        icon={
                          <ThumbDownOutlinedIcon color={colors.grey[300]} />
                        }
                        checkedIcon={<ThumbDownIcon color={"inherit"} />}
                        color="secondary"
                      />
                    }
                  />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={9}>
              <Typography lineHeight={"40px"}>{feedbackQustions[1]}</Typography>
            </Grid>
            <Grid item xs={3} padding={"0px"}>
              <FormControl>
                <RadioGroup
                  row
                  aria-labelledby="demo-row-radio-buttons-group-label"
                  name="row-radio-buttons-group"
                  onChange={(e) => {
                    e.preventDefault();
                    formValues.appropriate = e.target.value;
                    setFormValues(formValues);
                  }}
                >
                  <FormControlLabel
                    value="yes"
                    control={
                      <Radio
                        icon={<ThumbUpOutlinedIcon color={colors.grey[300]} />}
                        checkedIcon={<ThumbUpIcon color={colors.grey[300]} />}
                        color="secondary"
                      />
                    }
                  />
                  <FormControlLabel
                    value="no"
                    control={
                      <Radio
                        icon={
                          <ThumbDownOutlinedIcon color={colors.grey[300]} />
                        }
                        checkedIcon={<ThumbDownIcon color={"inherit"} />}
                        color="secondary"
                      />
                    }
                  />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={9}>
              <Typography lineHeight={"40px"}>{feedbackQustions[2]}</Typography>
            </Grid>
            <Grid item xs={3} padding={"0px"}>
              <FormControl>
                <RadioGroup
                  row
                  aria-labelledby="demo-row-radio-buttons-group-label"
                  name="row-radio-buttons-group"
                  onChange={(e) => {
                    e.preventDefault();
                    formValues.factual_accurate = e.target.value;
                    setFormValues(formValues);
                  }}
                >
                  <FormControlLabel
                    value="yes"
                    control={
                      <Radio
                        color="secondary"
                        icon={<ThumbUpOutlinedIcon color={colors.grey[300]} />}
                        checkedIcon={<ThumbUpIcon color={colors.grey[300]} />}
                      />
                    }
                  />
                  <FormControlLabel
                    value="no"
                    color={colors.grey[300]}
                    control={
                      <Radio
                        color="secondary"
                        icon={
                          <ThumbDownOutlinedIcon color={colors.grey[300]} />
                        }
                        checkedIcon={<ThumbDownIcon color={"inherit"} />}
                      />
                    }
                  />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={9}>
              <TextField
                id="filled-multiline-static"
                label="Additional Feedback"
                multiline
                rows={4}
                fullWidth
                variant="filled"
                onChange={(e)=>{
                  e.preventDefault();
                  formValues.comment = e.target.value;
                }}
              />
            </Grid>
            <Grid item xs={3} padding={"0px"}></Grid>

            <Grid item xs={8}></Grid>
            <Grid item xs={4} padding={"0px"}>
              <Box
                display={"flex"}
                justifyContent={"flex-end"}
                justifyItems={"flex-end"}
                mt={"10px"}
              ></Box>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button sx={{ color: colors.grey[100] }} onClick={handleClose}>
            Cancel
          </Button>
          <Button sx={{ color: colors.grey[100] }} onClick={handleSubmit}>
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
```
