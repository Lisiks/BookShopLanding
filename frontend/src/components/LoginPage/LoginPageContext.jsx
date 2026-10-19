import { createContext } from "react";

const LoginPageContext = createContext({});

const LoginPageContextProvider = (props) => {
    const {children} = props;

    return (
        <LoginPageContext.Provider
            value={{}}
        >
            {children}
        </LoginPageContext.Provider>
    )
}

export default LoginPageContextProvider;