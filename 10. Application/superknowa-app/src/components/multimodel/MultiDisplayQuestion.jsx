import { Grid, Box, Button } from "@mui/material";
import { useSelector } from "react-redux";
import MultiSidebar from "./MultiSidebar";
import MultipleResult from "./MultipleResult";
import Footer from "../global/Footer";
import { useParams } from "react-router-dom";
import MultipleResultHistory from "./MultipleResultHistory";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const MultiDisplayQuestion = () => {
  //const theme = useTheme();
  //const colors = tokens(theme.palette.mode);

  const { question_id } = useParams();
  const { results } = useSelector((state) => state.multiDisplayAnswer);

  return (
    <Grid container spacing={0}>
      {/* Left navigation bar */}
      <MultiSidebar />
      {/* Top Navigation and content */}

      {results.length > 0 && (
        <Grid item xs={10} marginTop={"90px"}>
          <Box
            display={"flex"}
            justifyContent={"flex-end"}
            marginRight={"150px"}
          >
            {" "}
            <Button
              variant="outlined"
              color="inherit"
              component={Link}
              to={"/multimodel/"}
            >
              Back
            </Button>{" "}
          </Box>
          <MultipleResultHistory
            result={results[question_id]}
            question={results[question_id][0].question}
          />
        </Grid>
      )}
      <Footer />
    </Grid>
  );
};

export default MultiDisplayQuestion;
