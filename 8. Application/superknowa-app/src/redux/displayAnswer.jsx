import { createSlice } from "@reduxjs/toolkit";

export const displayAnswerSlice = createSlice({
    name: "displayAnswer",
    initialState: {
        results: []
    },
    reducers: {
        addMessages: (state, action) => {
            state.results = [...state.results, action.payload];
        }
    }
});

export const { addMessages } = displayAnswerSlice.actions;

export default displayAnswerSlice.reducer;