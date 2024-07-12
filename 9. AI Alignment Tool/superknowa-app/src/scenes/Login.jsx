import { Box, Button, Typography, Link } from "@mui/material";
import React from "react";
import IBMIcon from "../components/icons/IBMIcon";
import Footer from "../components/global/FooterV1";

const Login = ({ handleLogin }) => {

  return (
    <Box flexDirection={'column'} display={"flex"} justifyItems={"center"} justifyContent={"center"}>
      <Box
        display={"flex"}
        justifyItems={"center"}
        justifyContent={"center"}
        flexDirection={"row"}
      >
        <Box
          display={"flex"}
          justifyItems={"center"}
          justifyContent={"center"}
          flexDirection={"column"}
          mt={"200px"}
          width={"500px"}
        >
          <Box display={"flex"}
            justifyContent={"center"}
            justifyItems={"center"}>
          <Typography>
        <IBMIcon />
      </Typography>
          </Box>
          <Box
            display={"flex"}
            justifyContent={"center"}
            justifyItems={"center"}
          >
            <Typography
              fontWeight={"600"}
              fontSize={"2.2rem"}
              lineHeight={"2.5rem"}
            >
              Superknowa application
            </Typography>
          </Box>
          <Box
            display={"flex"}
            justifyContent={"center"}
            justifyItems={"center"}
          >
            <Typography
              fontSize={"18px"}
            >
              Click the login button to log in with your IBMid.
            </Typography>
          </Box>
          <Box
            display={"flex"}
            justifyContent={"center"}
            justifyItems={"center"}
            mt={'20px'}
          >
            <Button
              sx={{ width: 250, height: 40, backgroundColor: '#0653E9' }}
              size="large"
              variant="contained"
              onClick={handleLogin}
            >
              Login
            </Button>
          </Box>
          <Box
            display={"flex"}
            justifyContent={"center"}
            justifyItems={"center"}
            mt={'20px'}
          >
            <Typography fontSize={"16px"}>Don't have an account?</Typography>
          </Box>
          <Box
            display={"flex"}
            justifyContent={"center"}
            justifyItems={"center"}
            mt={'20px'}
          >
            <Button
              sx={{ width: 250, height: 40, textTransform: 'capitalize' }}
              size="large"
              variant="outlined"
              component={Link}
              href="https://www.ibm.com/account/reg/us-en/signup?formid=urx-19776&target=https%3A%2F%2Flogin.ibm.com%2Foidc%2Fendpoint%2Fdefault%2Fauthorize%3FqsId%3Df6c9d92c-37e6-4c93-9ba3-ec3b89cc403f%26client_id%3DOGQzYWY3MWQtZjc0YS00"              
            >
              Create an IBMid
              
            </Button>
          </Box>
        </Box>
      </Box>
      <Box marginTop={'100px'}>
        <Footer />
      </Box>
    </Box>
  );
};

export default Login;
