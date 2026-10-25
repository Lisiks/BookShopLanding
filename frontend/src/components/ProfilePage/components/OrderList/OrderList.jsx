import { useContext } from "react";

import Order from "../Order/Order";
import { ProfilePageContext } from "../../ProfilePageContext";

import "./styles.css"

const OrderList = () => {
    const {orderList, setPageObserveRef} = useContext(ProfilePageContext);



    return (
        <div className="profile-page-order-list">
            {orderList.map((orderData, orderListIdx) =>
                <Order 
                    key={`order-${orderData.id}`}
                    orderId={orderData.id}
                    orderDate={orderData.datetime.split("T")[0]}
                    orderShop={orderData.shop}
                    orderStatus={orderData.status}
                    orderItems={orderData.items}
                    ref={orderListIdx === orderList.length - 1 ? setPageObserveRef : null}
                />
            )}
        </div>
    );
}

export default OrderList;