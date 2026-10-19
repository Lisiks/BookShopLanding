import { createContext, useState } from "react";
import AddWindow from "../base/AddWindow/AddWindow";


export const BookPageContext = createContext({});

const BookPageContextProvider = (props) => {
    const {children} = props;

    const books = {
        "1": {
            bookId: "1", 
            bookImageUrl: "https://img06.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/b/14/b1442445ceb0cdac66e0f6375782279c.png", 
            bookTitle: "Воды Мира", 
            bookAuthor: "Самоделкин П.А.", 
            bookGenre: "Рассказ",
            bookYear: 1995,
            isbn: "43-5454-343-2",
            bookPrice: 126.99
        },
        
        "2": {
            bookId: "2", 
            bookImageUrl: "https://img06.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/b/14/b1442445ceb0cdac66e0f6375782279c.png", 
            bookTitle: "Воды Мира", 
            bookAuthor: "Самоделкин П.А.", 
            bookGenre: "Рассказ",
            bookYear: 1994,
            isbn: "43-2354-343-2",
            bookPrice: 250.99
        },

        "3": {
            bookId: "3", 
            bookImageUrl: "https://img06.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/b/14/b1442445ceb0cdac66e0f6375782279c.png", 
            bookTitle: "Воды Мира", 
            bookAuthor: "Самоделкин П.А.", 
            bookGenre: "Рассказ",
            bookYear: 1895,
            isbn: "12-5454-343-2",
            bookPrice: 199.99
        },    
    };

    const bookMap = new Map(Object.entries(books));
    const bookList = Array.from(bookMap.values());

    const authorsList = [
        {id: 1, f: "Михеев", i: "Аркадий", o: "Залутович"},
        {id: 2, f: "Трахичев", i: "Бубер", o: "Залутович"}
    ]

    const jahnreList = [
        {id: 1, name: "Проза"},
        {id: 2, name: "Роман"}
    ]



    const [selectedBookId, setSelectedBookId] = useState(null);
    const selectedBookData = bookMap.get(selectedBookId);



    const selectBook = (bookId) => {
        setSelectedBookId(bookId);
    }

    const deselectBook = () => {
        setSelectedBookId(null);
    }

    const addBook = (count) => {
        setSelectedBookId(null);
    }



    return (
        <BookPageContext.Provider value={
            {
                "bookList": bookList,
                "selectBook": selectBook,
                "authorsList": authorsList,
                "jahnreList": jahnreList
            }
        }>
            {children}
            {selectedBookId !== null && 
                <AddWindow
                    bookPrice={selectedBookData.bookPrice}
                    bookImageUrl={selectedBookData.bookImageUrl}
                    onAdd={addBook}
                    onClose={deselectBook}
                />
            }
        </BookPageContext.Provider>
    );
};

export default BookPageContextProvider;