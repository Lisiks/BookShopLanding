import { Link } from "react-router";
import BrownButton from "../../../base/BrownButton/BrownButton";
import InputLabel from "../../../base/InputLabel/InputLabel";

import "./styles.css"


const LoginForm = () => {
    return (
        <form className="login-form">
            <h1>Вход</h1>

            <InputLabel
                id="login-form-username-inp"
                name="username"
                inputType="text"
                inputMaxLength={30}
                labelText="Логин:"
            />

            <InputLabel
                id="login-form-password-inp"
                name="passwordPlain"
                inputType="password"
                inputMaxLength={72}
                labelText="Пароль:"
            />


            <Link to="/register" className="login-form-link">Нет аккаунта?</Link>

            <BrownButton type="submit">Войти</BrownButton>
        </form>
    )
}

export default LoginForm;