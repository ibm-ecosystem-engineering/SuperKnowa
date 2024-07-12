import { createSlice } from "@reduxjs/toolkit";

export const exampleQuestionSlicer = createSlice({
    name: "exampleQuestion",
    initialState: {
        exampleQuestion: ''
    },
    reducers: {
        setExampleQuestion: (state, action) => {
            state.exampleQuestion = action.payload;
        }
    }
});

export const { setExampleQuestion } = exampleQuestionSlicer.actions;

export default exampleQuestionSlicer.reducer;