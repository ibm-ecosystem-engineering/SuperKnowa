import {
  Box,
  Divider,
  Toolbar,
  Typography,
  Grid,
  useTheme,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import IBMIcon from "../icons/IBMIcon";
import { tokens } from "../../theme";
import { useDispatch, useSelector } from "react-redux";
import ChatBubbleOutlineSharpIcon from "@mui/icons-material/ChatBubbleOutlineSharp";
import { Link } from 'react-router-dom';

const MultiSidebar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { results } = useSelector((state) => state.multiDisplayAnswer);
  const dispatch = useDispatch(); 

  return (
    <Grid
      item
      xs={2}
      paddingTop={"80px"}
      color={"#FFFFFF"}
      sx={{ backgroundColor: "rgba(32,33,35)", height: "100vh" }}
    >
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"center"}
        height={"60px"}
      >
        <Typography variant="h4" lineHeight={"50px"}>
          History
        </Typography>
      </Box>
      <Divider style={{ backgroundColor: "#F7F7F8" }} />

      <Box display={"flex"}>
        <List style={{ fontSize: "12px", color: "#FFFFFF" }}>
          {results.map((item, i) => (
            <ListItem disablePadding key={i}>
              <ListItemButton component={Link} to={"/multimodel/" + i}
              >
                <ListItemIcon>
                  <ChatBubbleOutlineSharpIcon
                    style={{ color: "#FFFFFF", width: 20, height: 20 }}
                  />
                </ListItemIcon>
                <ListItemText primary={item.results.length > 0 ? item.results[0].question: ""} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Grid>
  );
};

export default MultiSidebar;
