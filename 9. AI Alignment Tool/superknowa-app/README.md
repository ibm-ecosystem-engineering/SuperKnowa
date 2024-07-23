# Getting Started with Superknowa Application

## Prerequisites

- [Node.js](https://nodejs.org/en) v18 or higher
- [IBM AppID](https://www.ibm.com/products/app-id) for application authentication
- A backend server to serve LLM Service, supported OpenAPI spec can be found [here](backend-openapi-document.json)

### IBM AppID Setup

Please provision an [IBM AppID instance](https://www.ibm.com/products/app-id) or replace the authentication with your choice. Modify the code in `App.js` as necessary.

```js
const appID = useMemo(() => {
  return new AppID();
}, []);

const handleLogin = async () => {
  try {
    const tokens = await appID.signin();
    const userInfo = await appID.getUserInfo(tokens.accessToken);
    sessionStorage.setItem("superknowa_user", JSON.stringify(userInfo));
    sessionStorage.setItem("superknowa_token", JSON.stringify(tokens));
    setUser(userInfo);
  } catch (e) {
    console.error(e);
    return [];
  }
};

const handleLogout = async () => {
  //await appID.logout();
  sessionStorage.removeItem("superknowa_user");
  sessionStorage.removeItem("superknowa_token");
  setUser(null);
}
```

### Environment Variables

Create a `.env` file to run the application with the following variables:

```sh
REACT_APP_PROFILE="dev"
REACT_APP_MULTI_NO_OF_MODEL=3
REACT_APP_CONTEXT_RETRIEVER=elastic
REACT_APP_IBM_AUTH_CLIENT_ID=
REACT_APP_IBM_AUTH_URL=
REACT_APP_BACKEND_BASE_URL=
```

### Backend Server

A backend server is required to communicate with watsonx.ai. Open API documentation is available in the root directory of the project as `backend-openapi-document.json`.

## Project Configuration and Details

- **Configuration**: Located in [src/api/config.jsx](src/api/config.jsx)
- **Landing Screen & Page Titles**: Controlled from [src/api/staticdb.jsx](src/api/staticdb.jsx)
- **Color and Theme**: Managed in [src/theme.js](src/theme.js)
- **Application State & Histories**: Stored in the Redux store [src/redux](src/redux)
- **Main Screens**: Located in [src/scenes](src/scenes)
- **Custom Components**: Found in [src/components](src/components)
- **Docker File**: Provided to build a container

## Available Scripts

To start the project, run the following commands in the project directory: `superknowa-app`

### Install Dependencies

```sh
npm install
```

### Start the Application

```sh
npm start
```
