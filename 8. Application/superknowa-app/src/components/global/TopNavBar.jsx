import { AppBar, useTheme } from "@mui/material";
import Topbar from "./TopBar";
import { tokens } from "../../theme";
import { ColorModeContext } from "react";

const TopNavBar = ({handleLogout}) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

    return (
        <AppBar style={{ backgroundColor: colors.primary[500], height: '70px', color: colors.grey[100]}}>
            <Topbar handleLogout={handleLogout} />
        </AppBar>
    );
}

export default TopNavBar;