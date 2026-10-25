import { Link } from "react-router";
import { useContext } from "react";
import { CartPageContext } from "../../CartPageContext";

import "./styles.css"
import BrownButton from "../../../base/BrownButton/BrownButton";

const Item = (props) => {
    const {bookId, bookTitle, bookCount, bookPrice} = props;

    const {incBookItemCount, decrBookItemCount, deleteBookItem} = useContext(CartPageContext);

    return (
        <div className="cart-page-item">
            <Link to={`/books/${bookId}`}>{bookTitle}</Link>
            <div className="cart-page-item-info">
                <BrownButton type="button" onClick={() => {decrBookItemCount(bookId)}}>-</BrownButton>
                <p className="cart-page-item-info-count">{bookCount}</p>
                <BrownButton type="button" onClick={() => {incBookItemCount(bookId)}}>+</BrownButton>
                <p className="cart-page-item-info-price">{(bookCount * bookPrice).toFixed(2)} руб.</p>
                <BrownButton type="button" className="item-delete-btn" onClick={() => {deleteBookItem(bookId)}}> </BrownButton>
            </div>
        </div>
    )
};

export default Item;