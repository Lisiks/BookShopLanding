import RegisterPageContextProvider from "./RegisterPageContext.jsx";
import RegisterForm from "./components/RegisterForm/RegisterForm.jsx";

import "./styles.css"


const RegisterPage = () => {
    return (
        <RegisterPageContextProvider>
            <title>Книжный мир: Регистрация</title>
            <main className="register-page-main">
                <RegisterForm/>
            </main>
        </RegisterPageContextProvider>
    )
}

export default RegisterPage;