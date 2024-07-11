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