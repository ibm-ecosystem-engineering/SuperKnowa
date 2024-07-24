import { createSlice } from "@reduxjs/toolkit";

export const trackingSlice = createSlice({
    name: "trackingInfo",
    initialState: {
        track: {
            "version": "Beta version"
        }
    },
    reducers: {
        setTracking: (state, action) => {
            state.track = action.payload;
        }
    }
});

export const { setTracking } = trackingSlice.actions;

export default trackingSlice.reducer;