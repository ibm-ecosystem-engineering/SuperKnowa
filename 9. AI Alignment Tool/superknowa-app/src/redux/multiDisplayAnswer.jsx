import { createSlice } from "@reduxjs/toolkit";

export const displayMultiAnswerSlice = createSlice({
    name: "multiDisplayAnswer",
    initialState: {
        results: []
    },
    reducers: {
        addMultiMessages: (state, action) => {
            state.results = [...state.results, action.payload];
        }
    }
});

export const { addMultiMessages } = displayMultiAnswerSlice.actions;

export default displayMultiAnswerSlice.reducer;