import BookViewPageContextProvider from "./BookViewPageContext";
import BookMain from "./components/BookMain/BooMain";


const BookViewPage = () => {
    return (
        <BookViewPageContextProvider>
            <BookMain/>
        </BookViewPageContextProvider>
    )
};

export default BookViewPage;