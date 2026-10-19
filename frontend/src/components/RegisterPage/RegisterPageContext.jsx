import { createContext } from "react";

const RegisterPageContent = createContext({});

const RegisterPageContextProvider = (props) => {
    const {children} = props;

    return (
        <RegisterPageContent.Provider
            value={{}}
        >
            {children}
        </RegisterPageContent.Provider>
    )
}

export default RegisterPageContextProvider;