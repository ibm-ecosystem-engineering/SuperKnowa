import {
  Box,
  Grid,
  useTheme,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import SidebarCustomContext from "../components/customContext/SidebarCustomContext";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { useSelector } from "react-redux";
import CustomContextChatButton from "../components/customContext/CustomContextChatButton";
import { tokens } from "../theme";
import { useState } from "react";
import Result from "../components/Result";
//import FooterV1 from "../components/global/FooterV1";

const HomeQnACustomContext = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { paragraph } = useSelector((state) => state.currentContext);
  const [results, setResults] = useState([]);

  return (
    <div>
      <Grid container spacing={0}>
        {/* Left navigation bar */}
        <SidebarCustomContext />
        {/* Top Navigation and content */}
        <Grid item xs={10} marginTop={"85px"} >
          <Grid container spacing={0}>
            <Grid item md={1}></Grid>
            <Grid item md={10}>
              {/* Accordion to display context returned  */}
              <Box display={"flex"} flexGrow={1} mt={"5px"} mb={"5px"}>
                <Accordion sx={{ width: "100%" }}>
                  <AccordionSummary
                    style={{
                      backgroundColor: colors.primary[400],
                    }}
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                  >
                    <Typography fontStyle={"italic"} fontSize={"16px"}>
                      Source document
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails
                    style={{
                      backgroundColor: colors.primary[500],
                    }}
                  >
                    <ul>
                      {paragraph.map((text, index) => (
                        <li key={index}>{text}</li>
                      ))}
                    </ul>
                  </AccordionDetails>
                </Accordion>
              </Box>
              {/* accordion end */}
              <div
                style={{
                  overflowY: "auto",
                  fontSize: "0.875rem",
                  lineHeight: "1.5rem",
                  fontWeight: "400",
                }}
              >
                {results.map((item, i) => (
                  <Result
                    typing={true} 
                    key={i} 
                    question={item.question} 
                    answer={item.answer} 
                    source={item.source} 
                    mongoRef={item.mongoRef}
                    model_id={item.model_id}
                    type={"custom_context"}
                  />
                ))}
              </div>
              <Box display={"flex"} justifyContent={"center"}>
                <CustomContextChatButton
                  setResults={setResults}
                  results={results}
                />
              </Box>
            </Grid>
            <Grid item md={1}></Grid>
            <Grid item md={12}>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
};

export default HomeQnACustomContext;
