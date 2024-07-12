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
import { tokens } from "../../theme";
import { useState } from "react";
import axios from "axios";
import { chat_custom_context_url } from "../../api/config";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { useRef } from "react";
import { addContextResults } from "../../redux/displayAnswerCurrentContext";

let controller;

const CustomContextChatButton = (props) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const dispatch = useDispatch();
  const inputRef = useRef(null);
  const { paragraph } = useSelector((state) => state.currentContext);

  const [lastQuestion, setLastQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    const question = inputRef.current.value;
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

  //const inputRef = useRef(null);

  const apiCall = (question, isGenerate) => {
    controller = new AbortController();

    question = question.trim();

    if (!question) return;

    if (!question.endsWith("?")) {
      var check = question.slice(-1);
      if (check === "." || check === "!") {
        let regex = /\./g;
        question = question.replace(regex, "?");
      } else {
        question = question + "?";
      }
    }

    // Set the conversation variable to true, so load conversation page
    setIsLoading(true); // conversation loading state to load conversation
    setLastQuestion(question); // set current question to a state for renerate answer button

    axios
      .post(
        chat_custom_context_url,
        {
          question: question,
          regenerate: isGenerate,
          paragraph: paragraph,
        },
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
          model_id: model_id,
        };

        dispatch(addContextResults(msg));
        setIsLoading(false);
        inputRef.current.value = "";
        const results = [...props.results, msg];
        props.setResults(results);
      })
      .catch((error) => {
        setIsLoading(false);

        if (error.code !== "ERR_CANCELED") {
          var errorMsg =
            "The information you are looking for is not available. Please try again later. Thank you.";
          dispatch(
            addContextResults({
              question: question,
              answer: errorMsg,
              source: undefined,
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
      {isLoading ? (
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
      )}

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
        inputRef={inputRef}
        onKeyDown={handleKeyDown}
      />
    </Box>
  );
};

export default CustomContextChatButton;
