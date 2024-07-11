import { createSlice } from "@reduxjs/toolkit";

export const currentCustomContextSlicer = createSlice({
    name: "currentContext",
    initialState: {
        paragraph: []
    },
    reducers: {
        setCurrentContext: (state, action) => {
            state.paragraph = action.payload;
        }
    }
});

export const { setCurrentContext } = currentCustomContextSlicer.actions;
export default currentCustomContextSlicer.reducer; 