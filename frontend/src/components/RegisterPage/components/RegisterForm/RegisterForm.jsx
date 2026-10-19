import { Link } from "react-router";
import BrownButton from "../../../base/BrownButton/BrownButton";
import InputLabel from "../../../base/InputLabel/InputLabel";

import "./styles.css"


const RegisterForm = () => {
    return (
        <form className="register-form">
            <h1>Регистрация</h1>

            <InputLabel
                id="register-form-username-inp"
                name="username"
                inputType="text"
                inputMaxLength={30}
                labelText="Логин:"
            />

            <InputLabel
                id="register-form-password-inp"
                name="passwordPlain"
                inputType="password"
                inputMaxLength={72}
                labelText="Пароль:"
            />

            <InputLabel
                id="register-form-password-repeat-inp"
                name="passwordConfirm"
                inputType="password"
                inputMaxLength={72}
                labelText="Повтор пароля:"
            />

            <Link to="/login" className="register-form-link">Есть аккаунт?</Link>

            <BrownButton type="submit">Зарегистрироваться</BrownButton>
        </form>
    )
}

export default RegisterForm;