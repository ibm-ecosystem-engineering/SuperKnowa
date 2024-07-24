import { Box, Typography, useTheme } from "@mui/material";
import IBMIcon from "../icons/IBMIcon";
import { tokens } from "../../theme";

const BuildLab = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box display={'flex'} >
      <Typography>
        <IBMIcon />
      </Typography>
      &nbsp; &nbsp;
      <Typography
        variant="h4"
        lineHeight={"30px"}
        alignSelf={'center'}
        noWrap
        component="a"
        href="/"
        sx={{
          mr: 2,
          display: { xs: "none", md: "flex" },
          fontWeight: 500,
          textDecoration: "none",
          color: colors.grey[100],
        }}
      >
        Ecosystem Engineering
      </Typography>
    </Box>
  );
};

export default BuildLab;
