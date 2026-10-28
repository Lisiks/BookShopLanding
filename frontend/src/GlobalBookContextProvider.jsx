import { createContext, useState, useEffect } from "react";
import QueryManager from "./query_manager";

export const GlobalBookContext = createContext({});

const GlobalBookContextPrivoder = (props) => {
    const {children} = props;

    const [bookMap, setBookMap] = useState(new Map());
    const [authorMap, setAuthorMap] = useState(new Map());
    const [genreMap, setGenreMap] = useState(new Map());

    const [bookSearchParams, setBookSearchParams] = useState(
        {page: 0}
    );

    const [bookAuthorId, setBookAuthorId] = useState("");
    const [bookGenreId, setBookGenreId] = useState("");
    const [bookTitle, setBookTitle] = useState("");
    const [bookMinPrice, setBookMinPrice] = useState("");
    const [bookMaxPrice, setBookMaxPrice] = useState("");

    const [abortController, setAbortCintroller] = useState(new AbortController());

    const [currentBookListScroll, setCurrentBookListScroll] = useState(0);

    useEffect(
        () => {
            Promise.all(
                [
                    QueryManager.getBooks(bookSearchParams, abortController.signal),
                    QueryManager.getAuthors(abortController.signal),
                    QueryManager.getGenres(abortController.signal),
                ]
            ).then(([bookData, authorsData, genresData]) => {
                setBookMap(new Map(Object.entries(bookData.responceBody)));
                setAuthorMap(new Map(Object.entries(authorsData.responceBody)));
                setGenreMap(new Map(Object.entries(genresData.responceBody)))
            })

            return () => {abortController.abort()}
        }, []
    )


    return(
        <GlobalBookContext.Provider value={{
            "bookMap": bookMap,
            "setBookMap": setBookMap,
            "bookSearchParams": bookSearchParams,
            "setBookSearchParams": setBookSearchParams,
            "bookAuthorId": bookAuthorId,
            "setBookAuthorId":setBookAuthorId,
            "bookGenreId": bookGenreId,
            "setBookGenreId":setBookGenreId,
            "bookTitle": bookTitle,
            "setBookTitle": setBookTitle,
            "bookMinPrice": bookMinPrice,
            "setBookMinPrice": setBookMinPrice,
            "bookMaxPrice": bookMaxPrice,
            "setBookMaxPrice": setBookMaxPrice,
            "authorMap": authorMap,
            "setAuthorMap": setAuthorMap,
            "genreMap": genreMap,
            "setGenreMap": setGenreMap,

            "currentBookListScroll": currentBookListScroll,
            "setCurrentBookListScroll": setCurrentBookListScroll
        }}>
            {children}
        </GlobalBookContext.Provider>
    )
}

export default GlobalBookContextPrivoder;