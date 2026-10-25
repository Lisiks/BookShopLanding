import Item from "../Item/Item";

import "./styles.css"

const ItemList = () => {
    const Items = [
        {id: 2, title: "Понос", count: 2, price: 230.43},
        {id: 3, title: "Понос2", count: 1, price: 330.43},
        {id: 4, title: "Понос3", count: 3, price: 630.43},
        {id: 2, title: "Понос", count: 2, price: 230.43},
        {id: 3, title: "Понос2", count: 1, price: 330.43},
        {id: 4, title: "Понос3", count: 333, price: 33630.43},
        {id: 2, title: "Понос", count: 2, price: 230.43},
        {id: 3, title: "Понос2", count: 1, price: 330.43},
        {id: 4, title: "Понос3", count: 3, price: 630.43},
    ]

    return (
        <div class="cart-page-item-list">
            {Items.map((itemData) => 
                <Item 
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
