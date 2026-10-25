import { useContext } from "react";
import { Link } from "react-router";

import { BookPageContext } from "../../BookPageContext";
import BrownButton from "../../../base/BrownButton/BrownButton";

import "./styles.css"



const API_ORIGIN = "http://localhost:8000";

const BookItem = (props) => {
    const {bookId, bookImageUrl, bookTitle, bookAuthor, bookGenre, bookYear, isbn, bookPrice, ref} = props;

    const {selectBook} = useContext(BookPageContext);

    return (
        <div className="book-item-block" ref={ref}>

            <div className="book-item-block-image-container">
                <img src={`${API_ORIGIN}/${bookImageUrl}`} alt="Обложка книги"/>
            </div>

            <div className="book-item-block-info-container">
                <div className="book-item-info-block">
                    <Link to={`/books/${bookId}`}>{bookTitle}</Link>
                    <p>Автор: {bookAuthor}</p>
                    <p>Жанр: {bookGenre}</p>
                    <p>Год: {bookYear}</p>
                    <p>ISBN: {isbn}</p>
                </div>
                
                <div className="book-item-price-block">
                    <p>Цена: {bookPrice} руб.</p>
                    <BrownButton type="button" onClick={() => {selectBook(bookId)}}> </BrownButton>
                </div>
            </div>
        </div>
    )
};

export default BookItem;