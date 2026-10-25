import QueryManager from "../../query_manager";

import { createContext, useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router";

export const ProfilePageContext = createContext({});


const ProfilePageContextProvider = (props) => {
    const {children} = props;


    const [orderMap, setOrderMap] = useState(new Map());

    const [page, setPage] = useState(0);
    const [pageIsLast, setPageIsLast] = useState(false);
    const [orderIsSearch, serOrderIsSearch] = useState(false)


    const [userData, setUserData] = useState({userId: 0, isBlocked: null, isAdmin: null, username: ""});
    const [logFormSubmit, setLogFormSubmit] = useState(false)

    const [abortController, setAbortCintroller] = useState(new AbortController());

    const navigate = useNavigate();


    useEffect(() => {
        Promise.all([
            QueryManager.me(abortController.signal),
            QueryManager.getOrders({"page": 0}, abortController.signal)
        ]).then(([meResponce, ordersResponce]) => {
            if (meResponce.responceStatus === 401) {
                navigate("/login");
                return;
            }

            setUserData(meResponce.responceBody);
            setOrderMap(new Map(Object.entries(ordersResponce.responceBody)));
        });
        
        return () => {abortController.abort()};
    }, []);

    const pageObserve = useRef(null);

    const setPageObserveRef = (node) => {
        if (node == null) {
            return;
        }

        if (pageObserve.current !== null) {
            pageObserve.current.disconnect();
        }

        pageObserve.current = new IntersectionObserver(([node]) => {
            if (node.isIntersecting) {
                pageScrollSearch()
            }
        });

        pageObserve.current.observe(node);
    }


    const pageScrollSearch = () => {
        if (pageIsLast || orderIsSearch) {
            return;
        }

        serOrderIsSearch(true);
        
        QueryManager.getOrders({"page": page + 1}, abortController.signal).then((responceData) => {
                console.log("Да")
                serOrderIsSearch(true);
                setPage(page + 1);


                if (Object.entries(responceData.responceBody).length === 0) {
                    setPageIsLast(true);
                    return;
                }

                const newOrderMap = structuredClone(orderMap)
                
                for (const [orderId, orderData] of Object.entries(responceData.responceBody)) {
                    newOrderMap.set(orderId, orderData);
                }
                setOrderMap(newOrderMap);
            }
        );
    }



    const logoutFormSubmit = async (event) => {
        event.preventDefault();

        if (logFormSubmit) {
            return;
        }

        setLogFormSubmit(true);

        QueryManager.logout().then( (logoutResponce) => {
            setLogFormSubmit(false);
            navigate("/")
        });
    }




    const orderList = Array.from(orderMap.values()).sort((a, b) => new Date(b.datetime) - new Date(a.datetime));

    return (
        <ProfilePageContext.Provider
            value={{
                "userData": userData,
                "logoutFormSubmit": logoutFormSubmit,

                "orderList": orderList,
                "setPageObserveRef": setPageObserveRef
            }}
        >
            {children}
        </ProfilePageContext.Provider>
    )
}

export default ProfilePageContextProvider;