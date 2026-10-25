import QueryManager from "../../query_manager";

import { useNavigate } from "react-router";
import { createContext, useState, useEffect } from "react";

export const RegisterPageContext = createContext({});

const RegisterPageContextProvider = (props) => {
    const {children} = props;

    const [formSubmit, setFormSubmit] = useState("");

    const [loginValue, setLoginValue] = useState("");
    const [passwordValue, setPasswordValue] = useState("");
    const [passwordConfirmValue, setPasswordConfirmValue] = useState("");


    const [loginIncorrectValue, setLoginIncorrectValue] = useState(false);
    const [passwordIncorrectValue, setPasswordIncorrectValue] = useState(false);
    const [passwordConfirmIncorrectValue, setPasswordConfirmIncorrectValue] = useState(false);

    const [loginIncorrectReason, setLoginIncorrectReason] = useState("");
    const [passwordIncorrectReason, setPasswordIncorrectReason] = useState("");
    const [passwordConfirmIncorrectReason, setPasswordConfirmIncorrectReason] = useState("");

    const abortController = new AbortController();

    const navigate = useNavigate();

    useEffect(() => {return () => {abortController.abort()}}, []);


    const inputLogin = (value) => {
        setLoginValue(value);
        setLoginIncorrectValue(false);
        setLoginIncorrectReason("");
    }

    const inputPasswordConfirm = (value) => {
        setPasswordConfirmValue(value);
        setPasswordConfirmIncorrectValue(false);
        setPasswordConfirmIncorrectReason("");
    }

    const inputPassword = (value) => {
        setPasswordValue(value);
        setPasswordIncorrectValue(false);
        setPasswordIncorrectReason("");
        
        setPasswordConfirmIncorrectValue(false);
        setPasswordConfirmIncorrectReason("");
    }

    

    
    const registerFormSubmit = (event) => {
        event.preventDefault();

        if (formSubmit) {
            return;
        }

        setFormSubmit(true);

        if (loginValue.length < 6 || loginValue.length > 30) {
            setLoginIncorrectValue(true);
            setLoginIncorrectReason("Некорректная длинна логина, необходимо от 6 до 30 символов");
            setFormSubmit(false);
            return;
        }

        if (passwordValue.length < 6 || passwordValue.length > 72) {
            setPasswordIncorrectValue(true);
            setPasswordIncorrectReason("Некорректная длинна пароля, необходимо от 6 до 72 символов");
            setFormSubmit(false);
            return;
        }

        if (passwordConfirmValue.length < 6 || passwordConfirmValue.length > 72) {
            setPasswordConfirmIncorrectValue(true);
            setPasswordConfirmIncorrectReason("Некорректная длинна пароля, необходимо от 6 до 72 символов");
            setFormSubmit(false);
            return;
        }

        if (passwordConfirmValue !== passwordValue) {
            setPasswordConfirmIncorrectValue(true);
            setPasswordConfirmIncorrectReason("Пароли не совпадают");
            setFormSubmit(false);
            return;
        }

        const registerFormdata = new FormData(event.target);

        QueryManager.register(registerFormdata, abortController.signal).then( (registerResponce) => {
            if (registerResponce.responceStatus === 201) {
                navigate("/login");
            } else if (registerResponce.responceStatus === 422) {
                alert("Введенные данные в соответсвии с валидацией формы.")
            } else if (registerResponce.responceStatus === 409) {
                setLoginIncorrectValue(true);
                setLoginIncorrectReason("Данный пользователь уже зарегестрирован");
            }
        });
        
        setFormSubmit(false);
    }


    return (
        <RegisterPageContext.Provider
            value={{
                "loginValue": loginValue,
                "passwordValue": passwordValue,
                "passwordConfirmValue": passwordConfirmValue,

                "loginIncorrectValue": loginIncorrectValue,
                "passwordIncorrectValue": passwordIncorrectValue,
                "passwordConfirmIncorrectValue": passwordConfirmIncorrectValue,

                "loginIncorrectReason": loginIncorrectReason,
                "passwordIncorrectReason": passwordIncorrectReason,
                "passwordConfirmIncorrectReason": passwordConfirmIncorrectReason,
                
                "inputLogin": inputLogin,
                "inputPassword": inputPassword,
                "inputPasswordConfirm": inputPasswordConfirm,

                "registerFormSubmit": registerFormSubmit
            }}
        >
            {children}
        </RegisterPageContext.Provider>
    )
}

export default RegisterPageContextProvider;