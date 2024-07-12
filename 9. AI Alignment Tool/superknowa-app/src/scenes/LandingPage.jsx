import * as React from "react";
import { Grid, Typography, useTheme } from "@mui/material";
import WbSunnyOutlinedIcon from "@mui/icons-material/WbSunnyOutlined";
import BoltOutlinedIcon from "@mui/icons-material/BoltOutlined";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import { tokens } from "../theme";
import { examples, limitations, suggestions } from "../api/staticdb";

export default function LandingPage(props) {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Grid container justify="center" mt={"60px"} p={"40px"} spacing={0}>
      <Grid item md={4}></Grid>
      <Grid item md={4} display={"flex"} justifyContent={"center"}>
        {props.text && <Typography variant="h2" mb={'10px'}>{props.text}</Typography>}
      </Grid>
      <Grid item md={4}></Grid>
      <Grid item md={4}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            textAlign: "center",
            marginBottom: "40px",
            fontSize: "1.125rem",
            lineHeight: "1.75rem",
          }}
        >
          <div
            style={{
              display: "block",
              flexDirection: "row",
              alignContent: "center",
              width: "100%",
              flexWrap: "wrap",
            }}
          >
            <WbSunnyOutlinedIcon />
          </div>
          Examples
        </div>

        {examples.map((question, i) => (
          <div
            style={{
              minWidth: "200px",
              backgroundColor: colors.primary[400],
              padding: "15px",
              margin: "10px",
              borderRadius: "5px",
              cursor: "pointer",
              fontSize: "0.85rem",
              lineHeight: "1.25rem",
            }}
            key={i}
            onClick={() => {
              props.inputRef.current.value = question;
            }}
          >
            {question}
          </div>
        ))}
      </Grid>
      <Grid item md={4}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            textAlign: "center",
            marginBottom: "40px",
            fontSize: "1.125rem",
            lineHeight: "1.75rem",
          }}
        >
          <div
            style={{
              display: "block",
              flexDirection: "row",
              alignContent: "center",
              width: "100%",
              flexWrap: "wrap",
            }}
          >
            <BoltOutlinedIcon />
          </div>
          Suggestions
        </div>

        {suggestions.map((suggestion, i) => (
          <div
            style={{
              minWidth: "200px",
              backgroundColor: colors.primary[400],
              padding: "15px",
              margin: "10px",
              borderRadius: "5px",
              fontSize: "0.85rem",
              lineHeight: "1.25rem",
            }}
            key={i}
          >
            {suggestion}
          </div>
        ))}
      </Grid>
      <Grid item md={4}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            textAlign: "center",
            marginBottom: "40px",
            fontSize: "1.125rem",
            lineHeight: "1.75rem",
          }}
        >
          <div
            style={{
              display: "block",
              flexDirection: "row",
              alignContent: "center",
              width: "100%",
              flexWrap: "wrap",
            }}
          >
            <InfoOutlinedIcon />
          </div>
          Limitations
        </div>

        {limitations.map((limitation, i) => (
          <div
            style={{
              minWidth: "200px",
              backgroundColor: colors.primary[400],
              padding: "15px",
              margin: "10px",
              borderRadius: "5px",
              fontSize: "0.85rem",
              lineHeight: "1.25rem",
            }}
            key={i}
          >
            {limitation}
          </div>
        ))}
      </Grid>
    </Grid>
  );
}
