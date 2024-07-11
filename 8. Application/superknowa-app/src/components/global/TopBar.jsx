import {
  Box,
  IconButton,
  Tooltip,
  useTheme,
  Typography,
  Link,
} from "@mui/material";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import { useContext } from "react";
import { ColorModeContext, tokens } from "../../theme";
import BuildLab from "./BuildLab";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import DrawerMenu from "./DrawerMenu";
import { useState } from "react";
import { useSelector } from "react-redux";
import GitHubIcon from "@mui/icons-material/GitHub";

const Topbar = ({handleLogout}) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const { track } = useSelector((state) => state.tracking);

  const handleDrawwerOpen = () => {
    if (drawerOpen) setDrawerOpen(false);
    else setDrawerOpen(true);
  };

  const handleDrawwerClose = (event) => {
    if (drawerOpen) setDrawerOpen(false);
  };

  return (
    <Box
      display={"flex"}
      justifyContent={"space-between"}
      p={0}
      onClick={handleDrawwerClose}
    >
      {/* IBM Build lab logo  */}
      <Box display={"flex"} width={"33%"}>
        <BuildLab />
      </Box>
      <Box
        display={"flex"}
        flexDirection={"column"}
        textAlign={"center"}
        width={"34%"}
      >
        <Typography
          fontWeight={"600"}
          fontSize={"1.8rem"}
          lineHeight={"2.5rem"}
        >
          IBM SuperKnowa
        </Typography>
        <Typography variant="h7">
          Ask me anything about any IBM product
        </Typography>
      </Box>

      <Box
        display={"flex"}
        justifyContent={"end"}
        width={"33%"}
        flexDirection={"row"}
      >
        <Box display={"flex"} justifyItems={"center"}>
          <Tooltip title="Display mode">
            <IconButton onClick={colorMode.toggleColorMode}>
              {theme.palette.mode === "dark" ? (
                <DarkModeOutlinedIcon />
              ) : (
                <LightModeOutlinedIcon />
              )}
            </IconButton>
          </Tooltip>
          <Tooltip title="Source code">
            <IconButton
              onClick={() => {
                window.open(
                  "https://github.com/ibm-ecosystem-engineering/SuperKnowa",
                  "_blank"
                );
              }}
            >
              <GitHubIcon />
            </IconButton>
          </Tooltip>

          <Box
            display={"flex"}
            flexDirection={"column"}
            justifyContent={"end"}
            marginRight={"10px"}
          >
            <Typography alignSelf={"end"}>
              {/* Alpha-3.0 version */}
              {track.version}
            </Typography>
            <Link
              href="https://github.com/ibm-ecosystem-engineering/SuperKnowa/issues"
              underline="none"
              alignSelf={"end"}
              color={colors.grey[100]}
              target="_blank"
            >
              Report an issue
            </Link>
          </Box>
          <Box
            lineHeight={"50px"}
            display={"flex"}
            flexDirection={"column"}
            justifyContent={"center"}
            ml={"10px"}
            mr={"20px"}
          >
            <MenuOutlinedIcon
              sx={{ cursor: "pointer" }}
              color="inherit"
              fontSize="large"
              onClick={handleDrawwerOpen}
            />
            <DrawerMenu
              open={drawerOpen}
              handleDrawwerOpen={handleDrawwerOpen}
              handleDrawwerClose={handleDrawwerClose}
              handleLogout={handleLogout}
            />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Topbar;
