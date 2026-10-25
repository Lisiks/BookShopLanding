import { useContext } from "react";

import { CartPageContext } from "../../CartPageContext";

import "./styles.css"

const OrderSum = () => {
    const {bookCartSum} = useContext(CartPageContext);

    return (
        <div className="cart-page-order-sum-block">
            <p>Итого: {bookCartSum} руб.</p>
        </div>
    )
};

export default OrderSum;