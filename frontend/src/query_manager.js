const API_ORIGIN = "http://localhost:8000";

class QueryManager {
    static sendResponce = async (url, signal, method, body, headers = {}) => {
        try {
            const responce = await fetch(
                url,
                {
                    method: method,
                    credentials: "include",
                    body: body,
                    signal: signal,
                    headers: headers
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

    static getBooks = async (queryParams, signal) => {
        const searchUrlParams = new URLSearchParams(queryParams)
        return await this.sendResponce(`${API_ORIGIN}/books/?${searchUrlParams.toString()}`, signal, "GET")
    }

    static getAuthors = async (signal) => {
        return await this.sendResponce(`${API_ORIGIN}/authors/`, signal, "GET")
    }

    static getGenres = async (signal) => {
        return await this.sendResponce(`${API_ORIGIN}/genres/`, signal, "GET")
    }

    static getShops = async (signal) => {
        return await this.sendResponce(`${API_ORIGIN}/shops/`, signal, "GET")
    }

    static getBooksByList = async (jsonBookList, signal) => {
        return await this.sendResponce(`${API_ORIGIN}/books/list`, signal, "POST", jsonBookList, {"Content-Type": "application/json"})
    }

    static createOrder = async (orderData, signal) => {
        return await this.sendResponce(`${API_ORIGIN}/orders/`, signal, "POST", orderData, {"Content-Type": "application/json"})
    }



    static login = async (loginFormData, signal) => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/login`, signal, "POST", loginFormData);
    }


    static register = async (registerFormData, signal) => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/`, signal, "POST", registerFormData);   
    }


    static logout = async (signal) => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/logout`, signal, "GET")
    }

    static me = async (signal) => {
        return await this.sendResponce(`${API_ORIGIN}/accounts/me`, signal, "GET")
    }
}


export default QueryManager;