# Getting Started with Superknowa Application

## Pre-requisite

- Nodejs v18 or up
- IBM AppID to add authentication to the application
- A Backend server to serve LLM Service

### Please provision an IBM AppID instance or replace the authentication with your choice. You have to remove/modify the code in `App.js`

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

### Environment variables needed are below. Please create a .env file to run the application

```sh
REACT_APP_PROFILE="dev"
REACT_APP_MULTI_NO_OF_MODEL=3
REACT_APP_CONTEXT_RETRIEVER=elastic
REACT_APP_IBM_AUTH_CLIENT_ID=
REACT_APP_IBM_AUTH_URL=
REACT_APP_BACKEND_BASE_URL=
```

### You need a backend server to communicate with watsonx.ai

Open API documentation can be found in root directory of the project `backend-openapi-document.json`

### Project Configuration and Details

- #### The configuration can be found in `src/api/config.jsx`

- #### Landing screen information and page titles can be controlled from here `src/api/staticdb.jsx`

- #### Color and theme are controlled by `src/theme.js`

- #### Application states and the histories are stored in redux store, the code can be found `src/redux`

- #### Main screens of application are  in the directory `src/scenes`

- #### All custom components are in the component directory `src/components`

- #### A docker file is provided to build a container

## Available Scripts

In the project directory, run the below command to start the project.

### `npm install`

### `npm start`

