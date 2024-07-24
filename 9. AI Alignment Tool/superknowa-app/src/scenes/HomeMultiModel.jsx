import { Grid, Box } from "@mui/material";
import { useSelector } from "react-redux";
import LandingPage from "./LandingPage";
import { useRef } from "react";
import Footer from "../components/global/Footer";
import MultipleResult from "../components/multimodel/MultipleResult";
import MultiSidebar from "../components/multimodel/MultiSidebar";
import MultiChatButton from "../components/multimodel/MultiChatButton";
import { appLabels } from "../api/staticdb";

const HomeMultiModel = () => {
  //const theme = useTheme();
  //const colors = tokens(theme.palette.mode);
  const inputRef = useRef(null);

  const { results } = useSelector((state) => state.multiDisplayAnswer);

  return (
    <Grid container spacing={0}>
      {/* Left navigation bar */}
      <MultiSidebar />
      {/* Top Navigation and content */}
      <Grid item xs={10} marginTop={"85px"}>
        {results.length > 0 && (
          <div
            style={{
              height: "71vh",
              overflowY: "auto",
              fontSize: "0.875rem",
              lineHeight: "1.5rem",
              fontWeight: "400",
            }}
          >
            {results.map((item, i) => (
              
              <MultipleResult
                typing={false}
                key={i}
                mongoRef={item.ref}
                model_id={item.model_id}
                result={item.results}
                question={item.results.length > 0 ? item.results[0].question: ""}
              />
            ))}
          </div>
        )}
        { /* results.length */ }
        {results.length < 1 && (
          <Grid container spacing={0}>
            <Grid item md={1}></Grid>
            <Grid item md={10}>
              <LandingPage text={appLabels.page_header_multi} inputRef={inputRef} />
            </Grid>
            <Grid item md={1}></Grid>
          </Grid>
        )}

        <Box display={"flex"} justifyContent={"center"}>
          <MultiChatButton inputRef={inputRef} />
        </Box>
      </Grid>
      <Footer />
    </Grid>
  );
};

export default HomeMultiModel;
