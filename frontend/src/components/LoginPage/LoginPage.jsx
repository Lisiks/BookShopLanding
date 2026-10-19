import LoginForm from "./components/LoginForm/LoginForm";
import LoginPageContextProvider from "./LoginPageContext";

import "./styles.css"

const LoginPage = () => {
    return (
        <LoginPageContextProvider>
            <title>Книжный мир: Вход</title>
            <main className="login-page-main">
                <LoginForm/>
            </main>
        </LoginPageContextProvider>
    );
}

export default LoginPage;