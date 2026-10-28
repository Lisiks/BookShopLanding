import { useContext } from "react";

import { Link } from "react-router";
import BrownButton from "../../../base/BrownButton/BrownButton";
import InputLabel from "../../../base/InputLabel/InputLabel";
import { RegisterPageContext } from "../../RegisterPageContext";

import "./styles.css"


const RegisterForm = () => {
    const {
        loginValue,
        passwordValue,
        passwordConfirmValue,

        loginIncorrectValue,
        passwordIncorrectValue,
        passwordConfirmIncorrectValue,

        loginIncorrectReason,
        passwordIncorrectReason,
        passwordConfirmIncorrectReason,
                
        inputLogin,
        inputPassword,
        inputPasswordConfirm,

        registerFormSubmit
    } = useContext(RegisterPageContext);


    return (
        <form className="register-form" onSubmit={registerFormSubmit}>
            <h1>Регистрация</h1>

            <InputLabel
                id="register-form-username-inp"
                name="username"
                inputType="text"
                inputMaxLength={30}
                labelText={"Логин: " + loginIncorrectReason}
                hasError={loginIncorrectValue}
                state={loginValue}
                setState={inputLogin}
            />

            <InputLabel
                id="register-form-password-inp"
                name="plainPassword"
                inputType="password"
                inputMaxLength={72}
                labelText={"Пароль: " + passwordIncorrectReason}
                hasError={passwordIncorrectValue}
                state={passwordValue}
                setState={inputPassword}
            />

            <InputLabel
                id="register-form-password-repeat-inp"
                inputType="password"
                inputMaxLength={72}
                labelText={"Повтор пароля: " + passwordConfirmIncorrectReason}
                hasError={passwordConfirmIncorrectValue}
                state={passwordConfirmValue}
                setState={inputPasswordConfirm}
            />

            <div className="register-form-link-block">
                <Link to="/" className="register-form-link">Назад</Link>
                <Link to="/login" className="register-form-link">Есть аккаунт?</Link>
            </div>

            

            <BrownButton type="submit">Зарегистрироваться</BrownButton>
        </form>
    )
}

export default RegisterForm;