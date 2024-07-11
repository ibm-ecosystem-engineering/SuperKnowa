import { createSlice } from "@reduxjs/toolkit";

export const displayAnswerCurrentContextSlice = createSlice({
    name: "displayAnswerCurrentContext",
    initialState: {
        results: []
    },
    reducers: {
        addContextResults: (state, action) => {
            state.results = [...state.results, action.payload];
        }
    }
});

export const { addContextResults } = displayAnswerCurrentContextSlice.actions;

export default displayAnswerCurrentContextSlice.reducer;