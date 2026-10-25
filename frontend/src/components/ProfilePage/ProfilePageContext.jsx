import QueryManager from "../../query_manager";

import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";

export const ProfilePageContext = createContext({});


const ProfilePageContextProvider = (props) => {
    const {children} = props;

    const [userData, setUserData] = useState({userId: 0, isBlocked: null, isAdmin: null, username: ""});
    const [logFormSubmit, setLogFormSubmit] = useState(false)

    const [abortController, setAbortCintroller] = useState(new AbortController());

    const navigate = useNavigate();


    useEffect(() => {
        QueryManager.me(abortController.signal).then(
            (meResponce) => {
                if (meResponce.responceStatus === 401) {
                    navigate("/login");
                } else {
                    setUserData(meResponce.responceBody);
                }
            }
        );
        return () => {abortController.abort()};
    }, []);

    const logoutFormSubmit = async (event) => {
        event.preventDefault();

        if (logFormSubmit) {
            return;
        }

        setLogFormSubmit(true);

        const logoutResponce = await QueryManager.logout();
        if (isNaN(logoutResponce.responceStatus)) {
            alert("Проблемы с подключением к серверу.");
        } else {
            navigate("/")
        }

        setLogFormSubmit(false);
    }


    return (
        <ProfilePageContext.Provider
            value={{
                "userData": userData,
                "logoutFormSubmit": logoutFormSubmit
            }}
        >
            {children}
        </ProfilePageContext.Provider>
    )
}

export default ProfilePageContextProvider;