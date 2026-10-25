import { useContext } from "react";

import { CartPageContext } from "../../CartPageContext";

import "./styles.css"

const OrderSum = () => {
    const summ = 123.23

    return (
        <div className="cart-page-order-sum-block">
            <p>Итого: {summ} руб.</p>
        </div>
    )
};

export default OrderSum;