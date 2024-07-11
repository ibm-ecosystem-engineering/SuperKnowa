import { createSlice } from "@reduxjs/toolkit";

export const clickTrackerSlicer = createSlice({
    name: "clickTracker",
    initialState: {
        clickTracker: {
            inConversation: false,
            historyButton: false,
            chatButton: false
        }
    },
    reducers: {
        updateClickTracker: (state, action) => {
            state.clickTracker = action.payload;
        }
    }
});

export const { updateClickTracker } = clickTrackerSlicer.actions;

export default clickTrackerSlicer.reducer;