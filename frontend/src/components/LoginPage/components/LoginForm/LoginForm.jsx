import { useContext } from "react";

import { Link } from "react-router";
import BrownButton from "../../../base/BrownButton/BrownButton";
import InputLabel from "../../../base/InputLabel/InputLabel";

import { LoginPageContext } from "../../LoginPageContext";

import "./styles.css"


const LoginForm = () => {
    const {
        loginValue, 
        passwordValue,
        loginIncorrectValue,
        passwordIncorrectValue,
        loginIncorrectReason,
        passwordIncorrectReason,
        inputLogin,
        inputPassword,
        loginFormSubmit
    } = useContext(LoginPageContext);

    return (
        <form className="login-form" onSubmit={loginFormSubmit}>
            <h1>Вход</h1>

            <InputLabel
                id="login-form-username-inp"
                name="username"
                inputType="text"
                inputMaxLength={30}
                labelText={"Логин: " + loginIncorrectReason}
                hasError={loginIncorrectValue}
                state={loginValue}
                setState={inputLogin}
            />

            <InputLabel
                id="login-form-password-inp"
                name="plainPassword"
                inputType="password"
                inputMaxLength={72}
                labelText={"Пароль: " + passwordIncorrectReason}
                hasError={passwordIncorrectValue}
                state={passwordValue}
                setState={inputPassword}
            />


            <Link to="/register" className="login-form-link">Нет аккаунта?</Link>

            <BrownButton type="submit">Войти</BrownButton>
        </form>
    )
}

export default LoginForm;