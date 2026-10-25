import { useNavigate } from "react-router";

import { createContext, useState, useEffect } from "react";
import QueryManager from "../../query_manager";

export const CartPageContext = createContext({});

const CartPageContextProvider = (props) => {
    const {children} = props;

    const [booksCartInfo, setBooksCartInfo] = useState({});
    const [shopsMap, setShopsMap] = useState(new Map());

    const [shopId, setShopId] = useState("");
    const [shopIdIncorrectValue, setShopIdIncorrectValue] = useState(false);
    const [shopIdIncorrectReason, setShopIdIncorrectReason] = useState("");

    const [createOrderFormIsSubmit, setCreateOrderFormIsSubmit] = useState(false);

    const [abortController, setAbortCintroller] = useState(new AbortController());

    const navigate = useNavigate();

    useEffect(
        () => {
            const cartLocalstorageData = JSON.parse(localStorage.getItem("cart"));

            const bookIdsJsonList = JSON.stringify({ items: Array.from(Object.keys(cartLocalstorageData)) })

            Promise.all([
                QueryManager.getBooksByList(bookIdsJsonList, abortController.signal),
                QueryManager.getShops(abortController.signal)
            ]).then(
                ([selectedBookData, shopsData]) => {

                    const newBookCartInfo = {};
                    for (const cartItemId of Array.from(Object.keys(cartLocalstorageData))) {
                        if (!(cartItemId in selectedBookData.responceBody)) {
                            delete cartLocalstorageData[cartItemId];
                        } else {
                            newBookCartInfo[cartItemId] = {
                                id: cartItemId, 
                                title: selectedBookData.responceBody[cartItemId].title,
                                count: cartLocalstorageData[cartItemId], 
                                price: selectedBookData.responceBody[cartItemId].price
                            }
                        }
                    }
                    setBooksCartInfo(newBookCartInfo);
                    setShopsMap(new Map(Object.entries(shopsData.responceBody)));

                    localStorage.setItem("cart", JSON.stringify(cartLocalstorageData));
                }
            );

            return () => {abortController.abort()};
        }, 
    [])

    const bookCartInfoList = Array.from(Object.values(booksCartInfo));
    const shopsList = Array.from(shopsMap.values());


    const bookCartSum = bookCartInfoList.length > 0 ? bookCartInfoList.reduce((sum, item) => sum + item.count * item.price, 0).toFixed(2) : "0.00";


    const incBookItemCount = (itemId) => {
        const cartLocalstorageData = JSON.parse(localStorage.getItem("cart"));
        const newBookCartInfo = structuredClone(booksCartInfo);

        cartLocalstorageData[itemId] ++;
        newBookCartInfo[itemId].count ++;

        setBooksCartInfo(newBookCartInfo);
        localStorage.setItem("cart", JSON.stringify(cartLocalstorageData));

    };

    const decrBookItemCount = (itemId) => {
        const cartLocalstorageData = JSON.parse(localStorage.getItem("cart"));
        const newBookCartInfo = structuredClone(booksCartInfo);

        if (cartLocalstorageData[itemId] > 1) {
            cartLocalstorageData[itemId] --;
            newBookCartInfo[itemId].count --;

            setBooksCartInfo(newBookCartInfo);
            localStorage.setItem("cart", JSON.stringify(cartLocalstorageData));
        }

    };

    const deleteBookItem = (itemId) => {
        const cartLocalstorageData = JSON.parse(localStorage.getItem("cart"));
        const newBookCartInfo = structuredClone(booksCartInfo);

        delete cartLocalstorageData[itemId];
        delete newBookCartInfo[itemId];

        setBooksCartInfo(newBookCartInfo);
        localStorage.setItem("cart", JSON.stringify(cartLocalstorageData));
    }

    const clearCart = () => {
        const userConfirm = confirm("Вы уверены, что хотите очистить корзину?")
        if (userConfirm) {
            setBooksCartInfo({});
            localStorage.setItem('cart', JSON.stringify({}));
        }
    }


    const inputShopId = (value) => {
        setShopId(value);
        setShopIdIncorrectValue(false);
        setShopIdIncorrectReason("");
    }

    const createOrderFormSubmit = (event) => {
        event.preventDefault();

        if (createOrderFormIsSubmit) {
            return;
        }

        setCreateOrderFormIsSubmit(true);

        if (shopId === "") {
            setShopIdIncorrectValue(true);
            setShopIdIncorrectReason("Необходимо выбрать магазин сбора заказа.");
            setCreateOrderFormIsSubmit(false);
            return;
        }

        if (Object.values(booksCartInfo).length < 1) {
            alert("Корзина пуста.")
            setCreateOrderFormIsSubmit(false);
            return;
        }

        const userConfirm = confirm("Подтвердите создание заказа.")
        if (!userConfirm) {
            setCreateOrderFormIsSubmit(false);
            return;
        }

        const orderData = JSON.stringify({
            "shopId": shopId,
            "items": Array.from(Object.values(booksCartInfo)).map((itemData) => {
                    return {bookId: itemData.id, count: itemData.count }
                }
            )
        })

        QueryManager.createOrder(orderData, abortController.signal).then((responceData) => {
                setCreateOrderFormIsSubmit(false);
                if (responceData.responceStatus === 404) {
                    alert("Часть книг из вашего заказа более недоступна для продажи. Пожалуйста, обновите страницу.");
                } else if (responceData.responceStatus === 401) {
                    alert("Для создания заказа необходимо пройти процедуру аутентификации. Пожалуйста, перейдите на вкладку \"Профиль\" для входа в аккаунт.");
                } else if (responceData.responceStatus === 201) {
                    setBooksCartInfo({});
                    localStorage.setItem('cart', JSON.stringify({}));
                    navigate("/profile");
                }
                
            }
        )

        
    };

    return (
        <CartPageContext.Provider
            value={{
                "bookCartInfoList": bookCartInfoList,
                "shopsList": shopsList,
                "bookCartSum": bookCartSum,

                "incBookItemCount": incBookItemCount,
                "decrBookItemCount": decrBookItemCount,
                "deleteBookItem": deleteBookItem,
                "clearCart": clearCart,

                "shopId": shopId,
                "shopIdIncorrectValue": shopIdIncorrectValue,
                "shopIdIncorrectReason": shopIdIncorrectReason,
                "inputShopId": inputShopId,

                "createOrderFormSubmit": createOrderFormSubmit
            }}
        >
            {children}
        </CartPageContext.Provider>
    )
}

export default CartPageContextProvider;