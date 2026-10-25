import QueryManager from "../../query_manager";

import { createContext, useState, useEffect, useRef } from "react";
import AddWindow from "../base/AddWindow/AddWindow";
import BookSearchPanel from "./components/BookSearchPanel/BookSearchPanel";


export const BookPageContext = createContext({});

const BookPageContextProvider = (props) => {
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

    const [bookMaxPriceIncorrectValue, setBookMaxPriceIncorrectValue] = useState(false);
    const [bookMinPriceIncorrectValue, setBookMinPriceIncorrectValue] = useState(false);

    const [bookMaxPriceIncorrectReason, setBookMaxPriceIncorrectReason] = useState("");
    const [bookMinPriceIncorrectReason, setBookMinPriceIncorrectReason] = useState("");



    const [bookPageIsLast, setBookPageIsLast] = useState(false);
    const [bookIsSearch, setBookIsSearch] = useState(false);
    const [searchWindowOpen, setSearchWindowOpen] = useState(false);


    const [abortController, setAbortCintroller] = useState(new AbortController());


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

    const bookList = Array.from(bookMap.values());
    const authorList = Array.from(authorMap.values());
    const genreList = Array.from(genreMap.values());


    const openSearchWindow = () => {
        setSearchWindowOpen(true);
    }

    const closeSearchWindow = () => {
        setSearchWindowOpen(false);
    };



    const inputTitle = (value) => {
        setBookTitle(value)
    }

    const inputAuthor = (value) => {
        setBookAuthorId(value)
    }

    const inputGenre = (value) => {
        setBookGenreId(value)
    }

    const inputMaxPrice = (value) => {
        setBookMaxPrice(value);
        setBookMaxPriceIncorrectValue(false);
        setBookMaxPriceIncorrectReason("");
    }

    const inputMinPrice = (value) => {
        setBookMinPrice(value);
        setBookMinPriceIncorrectValue(false);
        setBookMinPriceIncorrectReason("");
    }


    const bookListDomRef = useRef(null);

    const submitSearchForm = (event) => {
        event.preventDefault();

        if (bookIsSearch) {
            return;
        }

        setBookIsSearch(true);

        const paramsObject = {page: 0};

        if (bookTitle.trim().length > 0) {
            paramsObject.title = bookTitle;
        }

        if (bookAuthorId !== "") {
            paramsObject.authorId = bookAuthorId;
        }

        if (bookGenreId !== "") {
            paramsObject.genreId = bookGenreId;
        }

        if (bookMaxPrice !== "") {
            const maxPriceNumber = Number(bookMaxPrice);
            if (isNaN(maxPriceNumber) || maxPriceNumber < 0.01 || maxPriceNumber > 99999999.99) {
                setBookMaxPriceIncorrectValue(true);
                setBookMaxPriceIncorrectReason("Цена должна быть положительным числом, не превышающим 99999999.99")

                setBookIsSearch(false);
                return;
            }
            paramsObject.maxPrice = Math.round(maxPriceNumber * 100) / 100;
        }


        if (bookMinPrice !== "") {
            const minPriceNumber = Number(bookMinPrice);
            if (isNaN(minPriceNumber) || minPriceNumber < 0.01 || minPriceNumber > 99999999.99) {
                setBookMinPriceIncorrectValue(true);
                setBookMinPriceIncorrectReason("Цена должна быть положительным числом, не превышающим 99999999.99")

                setBookIsSearch(false);
                return;
            }
            paramsObject.minPrice = Math.round(minPriceNumber * 100) / 100;
        }

        QueryManager.getBooks(paramsObject, abortController.signal).then(
            (bookData) => {
                setBookIsSearch(false);
                bookListDomRef.current.scrollTop = 0;
                setBookMap(new Map(Object.entries(bookData.responceBody)));
                setBookSearchParams(paramsObject);
                setBookPageIsLast(false)
                setSearchWindowOpen(false);
            }
        );
    }


    const pageObserve = useRef(null);

    const setPageObserveRef = (node) => {
        if (node === null) {
            return;
        }

        if (pageObserve.current !== null) {
            pageObserve.current.disconnect();
        }

        pageObserve.current = new IntersectionObserver(([node]) => {
            if (node.isIntersecting) {
                pageScrollSearch();
            }
        });

        pageObserve.current.observe(node);
    }



    const pageScrollSearch = () => {
        if (bookPageIsLast || bookIsSearch) {
            return;
        }

        setBookIsSearch(true);
        
        const newSearchParams = structuredClone(bookSearchParams);
        newSearchParams.page++;

        QueryManager.getBooks(newSearchParams, abortController.signal).then((responceData) => {
                setBookIsSearch(false);
                setBookSearchParams(newSearchParams);


                if (Object.entries(responceData.responceBody).length === 0) {
                    setBookPageIsLast(true);
                    return;
                }

                const newBookMap = structuredClone(bookMap)
                
                for (const [bookId, bookData] of Object.entries(responceData.responceBody)) {
                    newBookMap.set(bookId, bookData);
                }
                setBookMap(newBookMap);
            }
        );
    }



    const subParamsIsUse = Object.entries(bookSearchParams).length > 1;
    
    const clearSearchParams = (event) => {
        event.preventDefault();

        if (bookIsSearch) {
            return;
        }

        setBookIsSearch(true);
        const baseParams = {page: 0};

        QueryManager.getBooks(baseParams, abortController.signal).then((bookData) => {
                setBookTitle("");
                setBookAuthorId("");
                setBookGenreId("");
                setBookMinPrice("");
                setBookMaxPrice("");
                setBookIsSearch(false);

                bookListDomRef.current.scrollTop = 0;
                setBookMap(new Map(Object.entries(bookData.responceBody)));
                setBookSearchParams(baseParams);
                setBookPageIsLast(false);
            }
        );
        
    }

    
    


    const [selectedBookId, setSelectedBookId] = useState(null);
    const selectedBookData = bookMap.get(String(selectedBookId));

    const selectBook = (bookId) => {
        setSelectedBookId(bookId);
    }

    const deselectBook = () => {
        setSelectedBookId(null);
    }

    const addBook = (count) => {
        const cartData = JSON.parse(localStorage.getItem("cart")) ?? {};

        if (!(selectedBookId in Object.keys(cartData))) {

            if (Object.keys(cartData).length < 10) {
                cartData[selectedBookId] = count;
            } else {
                alert("В одном заказе допустимо наличие не более 10 позиций. Для изменения заказа перейдите в раздел \"Корзина\".")
            }

        } else {
            cartData[selectedBookId] += Number(count);
        }

        localStorage.setItem("cart", JSON.stringify(cartData));

        setSelectedBookId(null);
    }

    return (
        <BookPageContext.Provider value={
            {
                "bookList": bookList,
                "authorList": authorList,
                "genreList": genreList,

                "bookTitle": bookTitle,
                "bookAuthorId": bookAuthorId,
                "bookGenreId": bookGenreId,
                "bookMaxPrice": bookMaxPrice,
                "bookMinPrice": bookMinPrice,

                "bookMaxPriceIncorrectValue": bookMaxPriceIncorrectValue,
                "bookMinPriceIncorrectValue": bookMinPriceIncorrectValue,

                "bookMaxPriceIncorrectReason": bookMaxPriceIncorrectReason,
                "bookMinPriceIncorrectReason": bookMinPriceIncorrectReason,

                "inputTitle": inputTitle,
                "inputAuthor": inputAuthor,
                "inputGenre": inputGenre,
                "inputMaxPrice": inputMaxPrice,
                "inputMinPrice": inputMinPrice,

                "selectBook": selectBook,
                "openSearchWindow": openSearchWindow,
                "closeSearchWindow": closeSearchWindow,

                "submitSearchForm": submitSearchForm,
            

                "subParamsIsUse": subParamsIsUse,
                "clearSearchParams": clearSearchParams,
                "setPageObserveRef": setPageObserveRef,

                "bookListDomRef": bookListDomRef
            }
        }>
            {children}
            {selectedBookId !== null && 
                <AddWindow
                    bookPrice={selectedBookData.price}
                    bookImageUrl={selectedBookData.imageFilePath}
                    onAdd={addBook}
                    onClose={deselectBook}
                />
            }
            {searchWindowOpen && <BookSearchPanel/>}
        </BookPageContext.Provider>
    );
};

export default BookPageContextProvider;