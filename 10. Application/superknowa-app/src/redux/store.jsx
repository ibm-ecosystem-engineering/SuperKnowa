import { configureStore } from "@reduxjs/toolkit";
import displayAnswerReducer from "./displayAnswer"
import clickTracker from "./clickTracker"
import exampleQuestion from "./exampleQuestion";
import displayHistory from "./displayHistory";
import currentCustomContextReducer from "./currentCustomContext";
import displayAnswerCurrentContext from "./displayAnswerCurrentContext";
import multiDisplayAnswer from "./multiDisplayAnswer";
import tracking from "./tracking";
import loggedInUser from "./loggedInUser";

export default configureStore({
    reducer: {
        displayAnswer: displayAnswerReducer,
        clickTracker: clickTracker,
        exampleQuestion: exampleQuestion,
        displayHistory: displayHistory,
        currentContext: currentCustomContextReducer,
        currentContextResult: displayAnswerCurrentContext,
        multiDisplayAnswer: multiDisplayAnswer,
        tracking: tracking,
        loggedInUser: loggedInUser
    },
});