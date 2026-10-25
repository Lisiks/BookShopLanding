import { useContext } from "react";

import Item from "../Item/Item";
import { CartPageContext } from "../../CartPageContext";

import "./styles.css"

const ItemList = () => {
    const {bookCartInfoList} = useContext(CartPageContext);

    return (
        <div className="cart-page-item-list">
            {bookCartInfoList.map((itemData) => 
                <Item 
                    key={`cart-item-${itemData.id}`}
                    bookId={itemData.id} 
                    bookTitle={itemData.title} 
                    bookCount={itemData.count}
                    bookPrice={itemData.price}
                />
            )};
        </div>
    )
};

export default ItemList;
