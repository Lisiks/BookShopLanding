import { useNavigate } from "react-router";
import QueryManager from "../../query_manager";

import { createContext, useState, useEffect } from "react";


export const LoginPageContext = createContext({});

const LoginPageContextProvider = (props) => {
    const {children} = props;

    
    const [formSubmit, setFormSubmit] = useState("");

    const [loginValue, setLoginValue] = useState("");
    const [passwordValue, setPasswordValue] = useState("");

    const [loginIncorrectValue, setLoginIncorrectValue] = useState(false);
    const [passwordIncorrectValue, setPasswordIncorrectValue] = useState(false);

    const [loginIncorrectReason, setLoginIncorrectReason] = useState("");
    const [passwordIncorrectReason, setPasswordIncorrectReason] = useState("");

    const [abortController, setAbortCintroller] = useState(new AbortController());

    const navigate = useNavigate();

    useEffect(() => {return () => {abortController.abort()}}, []);


    const inputLogin = (value) => {
        setLoginValue(value);
        setLoginIncorrectValue(false);
        setLoginIncorrectReason("");
    }

    const inputPassword = (value) => {
        setPasswordValue(value);
        setPasswordIncorrectValue(false);
        setPasswordIncorrectReason("");
    }

    const loginFormSubmit = (event) => {
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

        const loginFormData = new FormData(event.target);

        QueryManager.login(loginFormData, abortController.signal).then( (loginResponce) => {
            setFormSubmit(false);
            if (loginResponce.responceStatus === 200) {
                navigate("/profile");
            } else if (loginResponce.responceStatus === 422) {
                alert("Введенные данные в соответсвии с валидацией формы.")
            } else if (loginResponce.responceStatus === 401) {
                setLoginIncorrectValue(true);
                setLoginIncorrectReason("Некорректное имя пользователя или пароль");
            } else if (loginResponce.responceStatus === 400) {
                navigate("/profile");
            }
        });

        
    }

    return (
        <LoginPageContext.Provider
            value={{
                "loginValue": loginValue,
                "passwordValue": passwordValue,

                "loginIncorrectValue": loginIncorrectValue,
                "passwordIncorrectValue": passwordIncorrectValue,

                "loginIncorrectReason": loginIncorrectReason,
                "passwordIncorrectReason": passwordIncorrectReason,
                
                "inputLogin": inputLogin,
                "inputPassword": inputPassword,

                "loginFormSubmit": loginFormSubmit
            }}
        >
            {children}
        </LoginPageContext.Provider>
    )
}

export default LoginPageContextProvider;