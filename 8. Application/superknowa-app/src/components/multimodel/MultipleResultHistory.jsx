import {
    Box,
    Grid,
    Button,
    Typography,
  } from "@mui/material";
  import PsychologyAltSharpIcon from "@mui/icons-material/PsychologyAltSharp";
  import WatsonIcon from "../icons/WatsonIcon";
  import {  useState } from "react";
  import Answer from "../Answer";
  import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
  import Snackbar from '@mui/material/Snackbar';
  
  const MultipleResultHistory = (props) => {
  
    const [messageOpen, setMessageOpen] = useState(false);
    const [drag, setDrag] = useState(false);
    const [orderChanged, setOrderChanged] = useState(false);
  
    const submitRanking = () => {
      setDrag(true)
      setMessageOpen(true)
    }
  
    const handleMessageClose = () => {
      setMessageOpen(false)
    }

    const process_result = () => {
        return props.result.map((item, index) => {
            return {
                id: index,
                content:  <Answer typing={false} q_id={index} answer={item.answer} source={item.source} title={index} mongo_ref_id={index} />
            }
        })
    }

    const [divOrder, setDivOrder] = useState(process_result());

    const handleDragEnd = (result) => {
      if (!result.destination) return; // Return if dropped outside the droppable area
      setOrderChanged(true);
      const newDivOrder = Array.from(divOrder);
      const [movedDiv] = newDivOrder.splice(result.source.index, 1);
      newDivOrder.splice(result.destination.index, 0, movedDiv);
  
      setDivOrder(newDivOrder);
    };
  
    return (
      <div>
        <Box display={"flex"} justifyContent={"center"} >
          {/* QUESTION */}
          <Grid container spacing={1} borderRadius={"5px"}>
            <Grid item xs={1} display={"flex"} justifyContent={"right"}>
              <PsychologyAltSharpIcon />
            </Grid>
            <Grid item xs={11}>{props.question}</Grid>
          </Grid>
        </Box>
  
        <Box display={"flex"} justifyContent={"center"} pt={"15px"}>
          {/* ANSWER */}
          <Grid container spacing={1} borderRadius={"10px"} >
            <Grid item xs={1} display={"flex"} justifyContent={"right"}>
              <WatsonIcon />
            </Grid>
            <Grid item xs={10}>
              <Grid container>
                <Grid item xs={1}>
                  <Grid container height={"100%"}>
                    <Grid item xs={12}>
                      <Box
                        height={"100%"}
                        alignItems="center"
                        display="flex"
                        justifyContent="center"
                      >
                        <Typography>Rank #1</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12}>
                      <Box
                        height={"100%"}
                        alignItems="center"
                        display="flex"
                        justifyContent="center"
                      >
                        <Typography>Rank #2</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12}>
                      <Box
                        height={"100%"}
                        alignItems="center"
                        display="flex"
                        justifyContent="center"
                      >
                        <Typography>Rank #3</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12}>
                      { ' ' }
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={11}>
                  <DragDropContext onDragEnd={handleDragEnd}>
                    <Droppable droppableId="divArea">
                      {(provided) => (
                        <div ref={provided.innerRef} {...provided.droppableProps}>
                          {process_result().map((divId, index) => (
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
                                  {divId.content}
                                </div>
                              )}
                            </Draggable>
                          ))}
                          {provided.placeholder}
                        </div>
                      )}
                    </Droppable>
                  </DragDropContext>
                  {orderChanged && (
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
                          vertical: 'top',
                          horizontal: 'center'
                        }}
                      />
                      <Button color="inherit" onClick={submitRanking} variant="outlined" disabled={drag}>Submit Feedback</Button>
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
  
  export default MultipleResultHistory;