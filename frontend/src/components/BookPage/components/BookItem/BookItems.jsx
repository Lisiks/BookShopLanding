import { useContext } from "react";
import { Link } from "react-router";

import { BookPageContext } from "../../BookPageContext";

import "./styles.css"

const BookItem = (props) => {
    const {bookId, bookImageUrl, bookTitle, bookAuthor, bookGenre, bookYear, isbn, bookPrice} = props;

    const {selectBook} = useContext(BookPageContext);

    return (
        <div className="book-item-block">

            <img src={bookImageUrl} alt="Обложка книги"/>

            <div>
                <div className="book-item-info-block">
                    <Link to={`/books/${bookId}`}>{bookTitle}</Link>
                    <p>Автор: {bookAuthor}</p>
                    <p>Жанр: {bookGenre}</p>
                    <p>Год: {bookYear}</p>
                    <p>ISBN: {isbn}</p>
                </div>
                
                <div className="book-item-price-block">
                    <p>Цена: {bookPrice} руб.</p>
                    <button type="button" onClick={() => {selectBook(bookId)}}>{"\t\t\t\t"}</button>
                </div>
            </div>
        </div>
    )
};

export default BookItem;