import { Box, Toolbar, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import * as React from "react";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import LogoDevOutlinedIcon from "@mui/icons-material/LogoDevOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import AccountCircleOutlinedIcon from "@mui/icons-material/AccountCircleOutlined";
import PsychologyAltOutlinedIcon from "@mui/icons-material/PsychologyAltOutlined";
import UploadOutlinedIcon from "@mui/icons-material/UploadOutlined";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { setTracking } from "../../redux/tracking";
import { profile } from "../../api/config";
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';

const DrawerMenu = ({ open, handleDrawwerOpen, handleDrawwerClose, handleLogout }) => {
  const theme = useTheme();
  const dispatch = useDispatch();
  const colors = tokens(theme.palette.mode);

  const list = () => (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={handleDrawwerClose}
      onKeyDown={handleDrawwerClose}
    >
      <Toolbar>
        <AccountCircleOutlinedIcon style={{ height: "50px", width: "50px" }} />
        <Typography fontSize={"25px"} ml={"5px"}>
          Superknowa
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            component={Link}
            to={"/"}
            onClick={(event) => {
              dispatch(setTracking({ version: "Alpha-3.0 version" }));
            }}
          >
            <ListItemIcon>
              <HomeOutlinedIcon />
            </ListItemIcon>
            <ListItemText primary={"Home"} />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton
            component={Link}
            to={"/customcontext"}
            onClick={(event) => {
              dispatch(setTracking({ version: "Singlefile version" }));
            }}
          >
            <ListItemIcon>
              <UploadOutlinedIcon />
            </ListItemIcon>
            <ListItemText primary={"Add your pdf file"} />
          </ListItemButton>
        </ListItem>

        {profile === "dev" && (
          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to={"/multimodel"}
              onClick={(event) => {
                dispatch(setTracking({ version: "Multi-model version" }));
              }}
            >
              <ListItemIcon>
                <PsychologyAltOutlinedIcon />
              </ListItemIcon>
              <ListItemText primary={"Multi model"} />
            </ListItemButton>
          </ListItem>
        )}

        {/* }
        <ListItem disablePadding>
          <ListItemButton>
            <ListItemIcon>
              <LogoDevOutlinedIcon />
            </ListItemIcon>
            <ListItemText primary={"Dev"} />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton>
            <ListItemIcon>
              <SettingsOutlinedIcon />
            </ListItemIcon>
            <ListItemText primary={"Settings"} />
          </ListItemButton>
        </ListItem>
  { */}
      </List>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            component={Link}
            to={"/"}
            onClick={(event) => {
              handleLogout();
            }}
          >
            <ListItemIcon>
              <LogoutOutlinedIcon />
            </ListItemIcon>
            <ListItemText primary={"Logout"} />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Drawer anchor="right" open={open}>
      {list()}
    </Drawer>
  );
};

export default DrawerMenu;
