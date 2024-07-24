import { Grid, Box } from "@mui/material"
import Sidebar from "../components/global/Sidebar";
import ChatButton from "../components/ChatButton";
import Result from "../components/Result";
import { useSelector } from "react-redux";
import LandingPage from './LandingPage'
import { useRef } from "react";
import DisplayResult from "../components/DisplayResult";
import Footer from "../components/global/Footer";

const Home = () => {

    const inputRef = useRef(null);

    const {clickTracker } = useSelector((state) => state.clickTracker);
    const {results } = useSelector((state) => state.displayAnswer);
    const {displayHistory } = useSelector((state) => state.displayHistory);


    return (
            <Grid container spacing={0}>
                { /* Left navigation bar */ }
                    <Sidebar/>
                { /* Top Navigation and content */ }
                <Grid item xs={10} marginTop={'85px'} >
                    { /* User in conversation then display result page */ }
                    {clickTracker.inConversation ? (

                        clickTracker.historyButton ? (
                            <Result question={displayHistory.question} answer={displayHistory.answer} source={displayHistory.source} />
                        ): (
                            <DisplayResult results={results} />
                        )
                       
                    ):(
                        <Grid container spacing={0}>
                            <Grid item md={1}></Grid>
                            <Grid item md={10}><LandingPage inputRef={inputRef}/></Grid>
                            <Grid item md={1}></Grid>
                        </Grid>
                    )}
                    
                    <Box display={"flex"} justifyContent={"center"} >
                        <ChatButton inputRef={inputRef}/>
                    </Box>
                    
                </Grid>
                <Footer/>

            </Grid>
    )
}

export default Home;