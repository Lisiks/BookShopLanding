const API_ORIGIN = "http://localhost:8000";

class QueryManager {
    static login = async (loginFormData) => {
        try {
            const responce = await fetch(
                `${API_ORIGIN}/accounts/login`,
                {
                    method: "POST",
                    body: loginFormData
                }
            );

            return {
                "responceStatus": responce.status,
                "responceBody": await responce.json()
            }


        } catch (error) {
            return {
                "responceStatus": Number.NaN,
                "responceBody": {}
            };
        }
    }


    static register = async (registerFormData) => {
        try {
            const responce = await fetch(
                `${API_ORIGIN}/accounts/`,
                {
                    method: "POST",
                    body: registerFormData
                }
            );

            return {
                "responceStatus": responce.status,
                "responceBody": await responce.json()
            }
            
        } catch (error) {
            return {
                "responceStatus": Number.NaN,
                "responceBody": {}
            };
        }
        

        

        
    }
}


export default QueryManager;