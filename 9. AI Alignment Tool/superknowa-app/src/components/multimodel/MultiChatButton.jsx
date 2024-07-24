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
import { chat_multi_model_url } from "../../api/config";
import { useDispatch } from "react-redux";
import { addMultiMessages } from "../../redux/multiDisplayAnswer";

let controller;

const MultiChatButton = (props) => {
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

    setIsLoading(true); // conversation loading state to load conversation
    setLastQuestion(question); // set current question to a state for renerate answer button

    axios
      .post(
        chat_multi_model_url,
        { question: question, regenerate: isGenerate },
        { signal: controller.signal }
      )
      .then((response) => {
        const msg = response.data
        dispatch(addMultiMessages(msg));
        setIsLoading(false);
        props.inputRef.current.value = "";
      })
      .catch((error) => {
        setIsLoading(false);

        if (error.code !== "ERR_CANCELED") {
          var errorMsg =
            "The information you are looking for is not available. Please try again later. Thank you.";
          dispatch(
            addMultiMessages({
              "ref": undefined,
              "results":[
              {
              question: question,
              answer: errorMsg,
              source: undefined,
            }]})
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

export default MultiChatButton;
