import { useContext } from "react"

import { BookPageContext } from "../../BookPageContext"
import BookItem from "../BookItem/BookItems.jsx"

import "./styles.css"


const BookList = () => {
    const {bookList} = useContext(BookPageContext);
    return (
        <div className="book-page-book-list">
            {bookList.map((bookInfo) =>
                <BookItem 
                    bookId={bookInfo.bookId}
                    bookImageUrl={bookInfo.bookImageUrl}
                    bookTitle={bookInfo.bookTitle}
                    bookAuthor={bookInfo.bookAuthor}
                    bookGenre={bookInfo.bookGenre}
                    bookYear={bookInfo.bookYear}
                    isbn={bookInfo.isbn}
                    bookPrice={bookInfo.bookPrice}
                    key={`book-${bookInfo.bookId}`}
                />
            )}
        </div>        
    )
};

export default BookList;