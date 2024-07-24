import {
  Box,
  Divider,
  Typography,
  Grid,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import ChatBubbleOutlineSharpIcon from "@mui/icons-material/ChatBubbleOutlineSharp";
import { setDisplayHistory } from "../../redux/displayHistory";
import { updateClickTracker } from "../../redux/clickTracker";

const SidebarCustomContext = () => {
  const { results } = useSelector((state) => state.currentContextResult);
  const dispatch = useDispatch();

  return (
    <Grid 
      item
      xs={2}
      paddingTop={"80px"}
      color={"#FFFFFF"}
      sx={{ backgroundColor: "rgba(32,33,35)", height: '100vh' }}
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
              <ListItemButton
                onClick={(event) => {
                  dispatch(
                    setDisplayHistory({
                      question: item.question,
                      answer: item.answer,
                      source: item.source
                    })
                  );

                  dispatch(
                    updateClickTracker({
                      inConversation: true,
                      historyButton: true,
                      chatButton: false,
                    })
                  );
                }}
              >
                <ListItemIcon>
                  <ChatBubbleOutlineSharpIcon
                    style={{ color: "#FFFFFF", width: 20, height: 20 }}
                  />
                </ListItemIcon>
                <ListItemText primary={item.question} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Grid>
  );
};

export default SidebarCustomContext;
