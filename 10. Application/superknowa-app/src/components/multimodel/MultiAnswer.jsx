import { Box, Grid, useTheme, Rating, Button, Link } from "@mui/material";
import { useState } from "react";
import { tokens } from "../../theme";

import AnswerFeedbackDialog from "../AnswerFeedbackDialog";
import CommentIcon from "@mui/icons-material/Comment";
import Tooltip from "@mui/material/Tooltip";
import { TypeAnimation } from 'react-type-animation';
import MultiAnswerRating from "./MultiAnswerRating";
import MultiAnswerFeedbackDialog from "./MultiAnswerFeedbackDialog";

const MultiAnswer = (
    { 
      typing,
      answer,
      model_id,
      source,
      title,
      setRatingValues,
      ratingValues,
      setFeedbackChange,
      setFeedbackReference,
      feedbackReference,
      mongoRef
      }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [open, setOpen] = useState(false);

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
        { typing && <TypeAnimation sequence={[answer]} speed={150} /> }
        { !typing && <span>{answer}</span> }
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
          <MultiAnswerFeedbackDialog
            open={open}
            handleClose={handleClose}
            answer={answer}
            model_id={model_id}
            mongoRef={mongoRef}
            title={title}
            feedbackReference={feedbackReference}
            setFeedbackReference={setFeedbackReference}
            type={"multi_model"}
          />
        </Box>
      </Grid>
      <Grid item xs={2}>
        <Box height={'100%'} display={'flex'} justifyContent={'space-between'} flexDirection={'column'}>
          <MultiAnswerRating 
            handleClickOpen={handleClickOpen} 
            model_id={model_id}
            mongoRef={mongoRef}
            setRatingValues={setRatingValues}
            ratingValues={ratingValues}
            feedbackReference={feedbackReference}
            setFeedbackReference={setFeedbackReference}
            setFeedbackChange={setFeedbackChange}
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

export default MultiAnswer;