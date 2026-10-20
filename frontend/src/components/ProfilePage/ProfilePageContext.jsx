import { createContext } from "react";

export const ProfilePageContext = createContext({});


const ProfilePageContextProvider = (props) => {
    const {children} = props;

    return (
        <ProfilePageContext.Provider
            value={{}}
        >
            {children}
        </ProfilePageContext.Provider>
    )
}

export default ProfilePageContextProvider;