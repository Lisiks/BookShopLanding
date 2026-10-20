const API_ORIGIN = "http://localhost:8000";

class QueryManager {
    static sendResponce = async (url, method, body) => {
        try {
            const responce = await fetch(
                url,
                {
                    method: method,
                    credentials: "include",
                    body: body
                    
                }
            )
            return {
                "responceStatus": responce.status,
                "responceBody": await responce.json()
            };
        } catch (error) {
            console.log(error.message)
            return {
                "responceStatus": Number.NaN,
                "responceBody": {}
            };
        };
    }

    static login = async (loginFormData) => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/login`, "POST", loginFormData);
    }


    static register = async (registerFormData) => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/`, "POST", registerFormData);   
    }


    static logout = async () => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/logout`, "GET")
    }

    static me = async () => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/me`, "GET")
    }
}


export default QueryManager;