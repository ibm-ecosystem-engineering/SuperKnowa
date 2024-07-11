import { createSlice } from "@reduxjs/toolkit";

export const loggedInUserSlicer = createSlice({
    name: "loggedInUser",
    initialState: {
        userInfo: null
    },
    reducers: {
        setUserInfo: (state, action) => {
            state.userInfo = action.payload;
        }
    }
});

export const { setUserInfo } = loggedInUserSlicer.actions;

export default loggedInUserSlicer.reducer;