import Header from "../base/Header/Header.jsx"
import BookList from "./components/BookList/BookList.jsx"
import BookSearchForm from "./components/BookSearchForm/BookSearchForm.jsx"
import AddWindow from "../base/AddWindow/AddWindow.jsx"

import BookPageContextProvider from "./BookPageContext.jsx"

import "./styles.css"

const BookPage = () => {



    return (
        <BookPageContextProvider>
            <title>Книжный мир: Каталог</title>
            <main className="book-page-main">
                <Header pageName="Каталог" />
                <BookSearchForm />
                <BookList />
            </main>
        </BookPageContextProvider>    
    )
}

export default BookPage;