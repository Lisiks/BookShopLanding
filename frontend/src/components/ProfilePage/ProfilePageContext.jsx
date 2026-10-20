import QueryManager from "../../query_manager";

import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";

export const ProfilePageContext = createContext({});


const ProfilePageContextProvider = (props) => {
    const {children} = props;

    const [userData, setUserData] = useState(null);
    const [logFormSubmit, setLogFormSubmit] = useState(false)

    const navigate = useNavigate();


    useEffect(() => {
        const fetchUserData = async () => {
            const meResponce = await QueryManager.me();
            if (isNaN(meResponce.responceStatus)) {
                alert("Проблемы с подключением к серверу.");
            } else if (meResponce.responceStatus === 401) {
                navigate("/login");
            } else {
                setUserData(meResponce.responceBody);
            }
        }
        fetchUserData();
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
            {userData !== null && children}
        </ProfilePageContext.Provider>
    )
}

export default ProfilePageContextProvider;