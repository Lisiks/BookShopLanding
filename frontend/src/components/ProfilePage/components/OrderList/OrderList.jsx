import Order from "../Order/Order";

import "./styles.css"

const OrderList = () => {
    const orderList = [
        {
            orderId: 324,
            orderDate: "12.12.2023",
            orderShop: {town: "Киров", street: "Ленина", housing: "43a"},
            orderStatus: "В сборке",
            orderItems: [
                {id: 2, title: "Крутая книга", count: 2, price: 120.00},
                {id: 3, title: "Крутая книга", count: 2, price: 120.00},
                {id: 12, title: "Крутая книга", count: 2, price: 120.00}
            ]
        
        },
        {
            orderId: 1324,
            orderDate: "12.12.2023",
            orderShop: {town: "Киров", street: "Ленина", housing: "43a"},
            orderStatus: "В сборке",
            orderItems: [
                {id: 2, title: "Крутая книга", count: 2, price: 120.00},
                {id: 3, title: "Крутая книга", count: 2, price: 120.00},
                {id: 12, title: "Крутая книга", count: 2, price: 120.00}
            ]
        
        },
        {
            orderId: 2324,
            orderDate: "12.12.2023",
            orderShop: {town: "Киров", street: "Ленина", housing: "43a"},
            orderStatus: "В сборке",
            orderItems: [
                {id: 2, title: "Крутая книга", count: 2, price: 120.00},
                {id: 3, title: "Крутая книга", count: 2, price: 120.00},
                {id: 12, title: "Крутая книга", count: 2, price: 120.00}
            ]
        
        }
    ]


    return (
        <div className="profile-page-order-list">
            {orderList.map((orderData) => 
                <Order 
                    key={`order-${orderData.orderId}`}
                    orderId={orderData.orderId}
                    orderDate={orderData.orderDate}
                    orderShop={orderData.orderShop}
                    orderStatus={orderData.orderStatus}
                    orderItems={orderData.orderItems}
                />
            )}
        </div>
    );
}

export default OrderList;