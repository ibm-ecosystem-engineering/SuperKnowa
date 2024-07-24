import { Box, Grid, useTheme, Button, Link } from "@mui/material";
import { useState } from "react";
import { tokens } from "../theme";
import AnswerFeedbackDialog from "./AnswerFeedbackDialog";
import CommentIcon from "@mui/icons-material/Comment";
import Tooltip from "@mui/material/Tooltip";
import AnswerRating from "./AnswerRating";
import { TypeAnimation } from 'react-type-animation';

const Answer = (
    { 
      answer, 
      question,
      source, 
      mongoRef, 
      model_id,
      typing,
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
        { typing && <TypeAnimation sequence={[answer]} speed={120} /> }
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
          <AnswerFeedbackDialog
            open={open}
            handleClose={handleClose}
            answer={answer}
            title={""}
            mongoRef={mongoRef}
            question={question}
            feedbackReference={feedbackReference}
            setFeedbackReference={setFeedbackReference}
            type={type}
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