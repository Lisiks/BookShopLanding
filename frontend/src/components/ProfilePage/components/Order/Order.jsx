import { useState } from "react";

import "./styles.css"

const Order = (props) => {
    const {
        orderId,
        orderDate,
        orderShop,
        orderStatus,
        orderItems,
        ref
    } = props;
    
    const [active, setActive] = useState(false);

    const orderSum = orderItems.reduce((sum, itemData) => sum + itemData.count * itemData.price, 0).toFixed(2);

    return (
        <div className="order" active={String(active)} onClick={() => {setActive(!active)}} ref={ref}>
            <div className="order-character">
                <p className="order-data-bold-paragraph">Заказ №{orderId}</p>
                <p className="order-data-bold-paragraph">{orderDate}</p>
            </div>
            
            <p className="order-data-paragraph">г. {orderShop.town}, ул. {orderShop.street}, {orderShop.housing}</p>
            <p className="order-data-paragraph">Статус: {orderStatus}</p>

            <div className="order-character">
                <p className="order-data-bold-paragraph">Сумма:</p>
                <p className="order-data-bold-paragraph">{orderSum} руб.</p>
            </div>

            <div className="order-product-list">
                <div>
                    <p>Книга</p>
                    <p>Стоимость</p>
                </div>

                {orderItems.map((itemData) => 
                    <div key={`order-${orderId}-item-${itemData.bookId}`}>
                        <p>{itemData.book.title} x{itemData.count}</p>
                        <p>{(itemData.count * itemData.price).toFixed(2)} руб.</p>
                    </div>
                )}                  
            </div>
        </div>
    )
}

export default Order;