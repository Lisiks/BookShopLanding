import ProfilePageContextProvider from "./ProfilePageContext";
import Header from "../base/Header/Header";
import UserData from "./components/UserData/UserData";
import OrderList from "./components/OrderList/OrderList";

import "./styles.css"



const ProfilePage = () => {
    return (
        <ProfilePageContextProvider>
            <title>Книжный мир: Профиль</title>
            <main className="profile-page-main">
                <Header pageName="Профиль"/>
                <UserData />
                <OrderList />
            </main>
        </ProfilePageContextProvider>
    );
};

export default ProfilePage;