import { createContext } from "react";

export const CartPageContext = createContext({});

const CartPageContextProvider = (props) => {
    const {children} = props;

    return (
        <CartPageContext.Provider
            value={{}}
        >
            {children}
        </CartPageContext.Provider>
    )
}

export default CartPageContextProvider;