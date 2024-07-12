import { Box, Grid, useTheme, Rating } from "@mui/material";
import { useState } from "react";
import StarIcon from "@mui/icons-material/Star";

const labels = {
  1: "Gibberish/Incorrect/Wrong",
  2: "Partially correct",
  3: "Correct but incomplete/truncated sentence",
  4: "Correct but Repetitive phrases/sentences",
  5: "Excellent",
};

function getLabelText(value) {
  return `${value} Star${value !== 1 ? "s" : ""}, ${labels[value]}`;
}

const MultiAnswerRating = ({
  handleClickOpen,
  setRatingValues,
  model_id,
  ratingValues,
  setFeedbackChange
}) => {
  const [value, setValue] = useState(-1);
  const [hover, setHover] = useState(-1);

  const handleFeedback = (feedback) => {
    setValue(feedback);

    let existingIndex = ratingValues.findIndex(
      (item) => item.model_id === model_id
    );

    if (existingIndex < 0) { // the rating is not saved, if index is -1
      setRatingValues([
        ...ratingValues,
        {
          star: feedback,
          model_id: model_id,
        },
      ]);
    } else { // new rating
      let temp = ratingValues;
      
      temp[existingIndex] = {
        star: feedback,
        model_id: model_id,
      };
      setRatingValues(temp);
    }
    setFeedbackChange(true);
    if (feedback < 2) handleClickOpen();
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

export default MultiAnswerRating;
