import * as React from "react";
import { ColorModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Home from "./scenes/Home";
import { Routes, Route } from "react-router-dom";
import TopNavBar from "./components/global/TopNavBar";
import HomeCustomContext from "./scenes/HomeCustomContext";
import HomeQnACustomContext from "./scenes/HomeQnACustomContext";
import HomeMultiModel from "./scenes/HomeMultiModel";
import MultiDisplayQuestion from "./components/multimodel/MultiDisplayQuestion";
import { useState, useMemo, useEffect } from "react";
import AppID from "ibmcloud-appid-js";
import Login from "./scenes/Login";

export default function App() {
  const [theme, colorMode] = useMode();
  const [user, setUser] = useState();

  const appID = useMemo(() => {
    return new AppID();
  }, []);

  const handleLogin = async () => {
    try {
      const tokens = await appID.signin();
      const userInfo = await appID.getUserInfo(tokens.accessToken);
      sessionStorage.setItem("superknowa_user", JSON.stringify(userInfo));
      sessionStorage.setItem("superknowa_token", JSON.stringify(tokens));
      setUser(userInfo);
    } catch (e) {
      console.error(e);
      return [];
    }
  };

  const handleLogout = async () => {
    //await appID.logout();
    sessionStorage.removeItem("superknowa_user");
    sessionStorage.removeItem("superknowa_token");
    setUser(null);
  }

  useEffect(() => {
    const loggedInUser = sessionStorage.getItem("superknowa_user");

    if (loggedInUser) {
      setUser(JSON.parse(loggedInUser));
    }

    (async () => {
      try {
        await appID.init({
          clientId: process.env.REACT_APP_IBM_AUTH_CLIENT_ID,
          discoveryEndpoint: process.env.REACT_APP_IBM_AUTH_URL,
        });
      } catch (e) {
        console.error(e);
      }
    })();
  }, [appID]);
  

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
          {user && <div className="app">
            <main className="content">
              <TopNavBar handleLogout={handleLogout} />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/multimodel" element={<HomeMultiModel />} />
                <Route
                  path="/multimodel/:question_id"
                  element={<MultiDisplayQuestion />}
                />
                <Route path="/customcontext" element={<HomeCustomContext />} />
                <Route
                  path="/qnacustomcontext"
                  element={<HomeQnACustomContext />}
                />
              </Routes>
            </main>
          </div>
          }
          {
            !user && <Login handleLogin={handleLogin}/>
          }
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}
