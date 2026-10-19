const API_ORIGIN = "http://localhost:8000";

class QueryManager {
    static login = async (loginFormData) => {
        const responce = await fetch(
            `${API_ORIGIN}/accounts/login`,
            {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: loginFormData
            }
        );

        if (responce.ok) {
            return await responce.json();
        };

        throw new Error("Incorrect Login Data!");
    }


    static register = async (registerFormData) => {
        const responce = await fetch(
            `${API_ORIGIN}/accounts/`,
            {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: registerFormData
            }
        );

        if (responce.ok) {
            return await responce.json();
        };

        throw new Error("Incorrect Register Data!");
    }
}


export default QueryManager;