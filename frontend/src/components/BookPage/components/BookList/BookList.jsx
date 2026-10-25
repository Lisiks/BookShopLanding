import { useContext } from "react"

import { BookPageContext } from "../../BookPageContext"
import BookItem from "../BookItem/BookItems.jsx"

import "./styles.css"


const BookList = () => {
    const {bookList, bookListDomRef, setPageObserveRef} = useContext(BookPageContext);


    return (
        <div className="book-page-book-list" ref={bookListDomRef}>
            {bookList.map((bookInfo, bookListIdx) =>
            
                <BookItem 
                    ref={bookListIdx === bookList.length - 1 ? setPageObserveRef : null}
                    bookId={bookInfo.id}
                    bookImageUrl={bookInfo.imageFilePath}
                    bookTitle={bookInfo.title}
                    bookAuthor={`${bookInfo.author.f} ${bookInfo.author.i[0]}. ${bookInfo.author.o[0]}.`}
                    bookGenre={bookInfo.genre.name}
                    bookYear={bookInfo.writeYear}
                    isbn={bookInfo.isbn}
                    bookPrice={Number(bookInfo.price).toFixed(2)}
                    key={`book-${bookInfo.id}`}
                />
            )}
        </div>        
    )
};

export default BookList;