import {
  Box,
  Grid,
  //useTheme,
  Button,
  Typography,
} from "@mui/material";
//import { tokens } from "../../theme";
import PsychologyAltSharpIcon from "@mui/icons-material/PsychologyAltSharp";
import WatsonIcon from "../icons/WatsonIcon";
import { useState } from "react";
import { chat_multi_no_model } from "../../api/config";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import Snackbar from "@mui/material/Snackbar";
import { saveMultiFeedback } from "../../api/feedback/feedback_api";
import MultiAnswer from "./MultiAnswer";

const MultipleResult = ({ result, question, model_id, mongoRef, typing }) => {
  //const theme = useTheme();
  //const colors = tokens(theme.palette.mode);

  const [messageOpen, setMessageOpen] = useState(false);
  const [drag, setDrag] = useState(false);
  const [feedbackChange, setFeedbackChange] = useState(false);

  const initialize_ratings = () => {
    return result.map((item) => {
      return {
        star: -1,
        model_id: item.model_id
      }
    })
  }

  const [ratingValues, setRatingValues] = useState(initialize_ratings);

  /*
    It will track down the reference of the mongo id, if feedback is already submitted or not
    if the value is existed, thats mean there is already a feedback submitted and we can use
    this reference id to submit more feedback/update feedback on the same reference.
  */
  const [feedbackReference, setFeedbackReference] = useState(null);

  const submitRanking = () => {
    setDrag(false);
    
    saveMultiFeedback(
        divOrder, 
        mongoRef, 
        result, 
        ratingValues, 
        feedbackReference, 
        setFeedbackReference, 
        question);
    setMessageOpen(true);
  };

  const handleMessageClose = () => {
    setMessageOpen(false);
  };

  /*
  Preparing the object for drag and drop and answering questions
  */
  const process_result = () => {
    return result.map((item, index) => {
      return {
        id: index,
        model_id: item.model_id,
        mongoRef: mongoRef,
        type: "multi_model",
        answer: item.answer,
        question: question,
        source: item.source,
      };
    });
  };

  /*
    It tracks down all the ranking, you can get updated information from this list `divOrder`
  */
  const [divOrder, setDivOrder] = useState(process_result());

  const handleDragEnd = (result) => {
    if (!result.destination) return; // Return if dropped outside the droppable area

    setFeedbackChange(true);
    const newDivOrder = Array.from(divOrder);
    const [movedDiv] = newDivOrder.splice(result.source.index, 1);
    newDivOrder.splice(result.destination.index, 0, movedDiv);
    setDivOrder(newDivOrder);
  };

  const RankingSideLabel = () => {
    let items = [];
    for (let i = 1; i <= chat_multi_no_model; i++) {
      items.push(
        <Grid key={i} item xs={12}>
          <Box
            height={"100%"}
            alignItems="center"
            display="flex"
            justifyContent="center"
          >
            <Typography>Rank #{i}</Typography>
          </Box>
        </Grid>
      );
    }
    return items;
  };

  return (
    <div>
      <Box display={"flex"} justifyContent={"center"}>
        {/* QUESTION */}
        <Grid container spacing={1} borderRadius={"5px"}>
          <Grid item xs={1} display={"flex"} justifyContent={"right"}>
            <PsychologyAltSharpIcon />
          </Grid>
          <Grid item xs={11}>
            {question}
          </Grid>
        </Grid>
      </Box>

      <Box display={"flex"} justifyContent={"center"} pt={"15px"}>
        {/* ANSWER */}
        <Grid container spacing={1} borderRadius={"10px"}>
          <Grid item xs={1} display={"flex"} justifyContent={"right"}>
            <WatsonIcon />
          </Grid>
          <Grid item xs={10}>
            <Grid container>
              <Grid item xs={1}>
                <Grid container height={"100%"}>
                  <RankingSideLabel />
                  <Grid item xs={12}>
                    {" "}
                  </Grid>
                </Grid>
              </Grid>
              <Grid item xs={11}>
                <DragDropContext onDragEnd={handleDragEnd}>
                  <Droppable droppableId="divArea">
                    {(provided) => (
                      <div ref={provided.innerRef} {...provided.droppableProps}>
                        {divOrder.map((divId, index) => (
                          <Draggable
                            key={divId.id}
                            draggableId={`div-${divId.id}`}
                            index={index}
                            isDragDisabled={drag}
                          >
                            {(provided) => (
                              <div
                                ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                              >
                                <MultiAnswer
                                  typing={typing}
                                  answer={divId.answer}
                                  model_id={divId.model_id}
                                  source={divId.source}
                                  title={index}
                                  setRatingValues={setRatingValues}
                                  ratingValues={ratingValues}
                                  setFeedbackChange={setFeedbackChange}
                                  mongoRef={mongoRef}
                                  feedbackReference={feedbackReference}
                                  setFeedbackReference={setFeedbackReference}
                                />
                              </div>
                            )}
                          </Draggable>
                        ))}
                        {provided.placeholder}
                      </div>
                    )}
                  </Droppable>
                </DragDropContext>
                {feedbackChange && (
                  <Box
                    display={"flex"}
                    flexDirection={"column"}
                    alignItems={"flex-end"}
                    ml={"20px"}
                    mt={"8px"}
                    mb={"5px"}
                  >
                    <Snackbar
                      open={messageOpen}
                      onClose={handleMessageClose}
                      message="Thank you for your feedback!"
                      sx={{ height: "100%" }}
                      anchorOrigin={{
                        vertical: "top",
                        horizontal: "center",
                      }}
                    />
                    <Button
                      color="inherit"
                      onClick={submitRanking}
                      variant="outlined"
                      disabled={drag}
                    >
                      Submit Feedback
                    </Button>
                  </Box>
                )}
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={1}></Grid>
        </Grid>
      </Box>
    </div>
  );
};

export default MultipleResult;
