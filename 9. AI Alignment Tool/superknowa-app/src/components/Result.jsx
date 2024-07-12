import { Box, Grid } from "@mui/material";
import PsychologyAltSharpIcon from "@mui/icons-material/PsychologyAltSharp";
import WatsonIcon from "./icons/WatsonIcon";
import Answer from "./Answer";

const Result = (
  {
    typing,
    question, 
    answer,
    source,
    mongoRef,
    model_id,
    type
  }
) => {


  return (
    <div style={{ paddingLeft: "50px", paddingRight: "50px", }}>
      <Box display={"flex"} justifyContent={"center"}>
        {/* QUESTION */}
        <Grid container spacing={1} borderRadius={"5px"} p={"10px"}>
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
        <Grid container spacing={1} borderRadius={"5px"} p={"10px"}>
          <Grid item xs={1} display={"flex"} justifyContent={"right"}>
            <WatsonIcon />
          </Grid>
          <Grid item xs={10}>
            <Answer 
              typing={typing} 
              question={question} 
              answer={answer} 
              source={source} 
              mongoRef={mongoRef} 
              model_id={model_id}
              type={type}
              />
          </Grid>
          <Grid item xs={1}>
          </Grid>
        </Grid>
      </Box>
    </div>
  );
};

export default Result;
