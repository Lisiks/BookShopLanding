import BrownButton from "../../../base/BrownButton/BrownButton";

import "./styles.css"

const UserData = () => {
    return (
        <form className="profile-page-user-data">
            <p>Пользователь: Lisiks</p>
            <BrownButton type="submit">Выйти</BrownButton>
        </form>
    )
}

export default UserData;