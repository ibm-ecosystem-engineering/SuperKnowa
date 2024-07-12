import { createSlice } from "@reduxjs/toolkit";

export const displayHistorySlicer = createSlice({
    name: "displayHistory",
    initialState: {
        displayHistory: {}
    },
    reducers: {
        setDisplayHistory: (state, action) => {
            state.displayHistory = action.payload;
        }
    }
});

export const { setDisplayHistory } = displayHistorySlicer.actions;

export default displayHistorySlicer.reducer;