import { useContext } from "react";
import BrownButton from "../../../base/BrownButton/BrownButton";
import { ProfilePageContext } from "../../ProfilePageContext";

import "./styles.css"

const UserData = () => {
    const {
        userData,
        logoutFormSubmit
    } = useContext(ProfilePageContext);

    return (
        <form className="profile-page-user-data" onSubmit={logoutFormSubmit}>
            <p>Пользователь: {userData.username}</p>
            <BrownButton type="submit">Выйти</BrownButton>
        </form>
    )
}

export default UserData;