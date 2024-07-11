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
import { tokens } from "../../theme";
import { useTheme } from "@mui/material";
import ThumbUpOutlinedIcon from "@mui/icons-material/ThumbUpOutlined";
import ThumbDownOutlinedIcon from "@mui/icons-material/ThumbDownOutlined";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import TextField from "@mui/material/TextField";
import { additionalFeedback, multiAdditionalFeedback } from "../../api/feedback/feedback_api";
import { Box, Grid, Typography } from "@mui/material";

const feedbackQustions = [
  "Is the response relevant and coherent?",
  "Was this a useful response with an appropriate amount of information?",
  "Is the response factual and accurate, based on the document?",
];

export default function MultiAnswerFeedbackDialog({
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
      additional_feedback: [{
        "model_id": model_id,
        "question": question,
        "answer": answer,
        "feedback": formValues
    }]}

    multiAdditionalFeedback(feedback,mongoRef,feedbackReference,setFeedbackReference)
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