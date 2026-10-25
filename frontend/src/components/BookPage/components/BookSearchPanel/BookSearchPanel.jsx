import { useContext, useRef, useEffect} from "react";

import InputLabel from "../../../base/InputLabel/InputLabel";
import SelectLabel from "../../../base/SelectLabel/SelectLabel";
import BrownButton from "../../../base/BrownButton/BrownButton";
import WhiteButton from "../../../base/WhiteButton/WhiteButton";
import {BookPageContext} from "../../BookPageContext";

import "./styles.css"

const BookSearchPanel = () => {
    const {
        closeSearchWindow, 
        authorList, 
        genreList,

        bookTitle,
        bookAuthorId,
        bookGenreId,
        bookMaxPrice,
        bookMinPrice,

        bookMaxPriceIncorrectValue,
        bookMinPriceIncorrectValue,

        bookMaxPriceIncorrectReason,
        bookMinPriceIncorrectReason,

        inputTitle,
        inputAuthor,
        inputGenre,
        inputMaxPrice,
        inputMinPrice,
        
        submitSearchForm
    } = useContext(BookPageContext);

    const searchWindow = useRef(null);

    useEffect(() => {
    
        const closeWindowCallback = (event) => {
            
            if (event.target === searchWindow.current) {
                closeSearchWindow();
            }
        };

        document.addEventListener('click', closeWindowCallback);

        return () => {document.removeEventListener('click', closeWindowCallback)};
    }, [])


    return (
        <div className="book-search-panel" ref={searchWindow}>
            <form className="books-search-panel-form" onSubmit={submitSearchForm}>
                <h2>Поиск книг:</h2>
                <InputLabel
                    id="book-search-panel-search-form-title-input"
                    name="bookTitle"
                    inputType="text"
                    inputMaxLength={100}
                    inputClassName="search-inp"
                    labelText="Название книги: "
                    state={bookTitle}
                    setState={inputTitle}
                />

                <SelectLabel
                    id="book-search-panel-search-form-author-input"
                    name="authorId"
                    labelText="Автор:"
                    placeHolderText="Выберите автора"
                    state={bookAuthorId}
                    setState={inputAuthor}
                >
                    {authorList.map((authorData) => 
                        <option value={authorData.id} key={`author-option-${authorData.id}`}>{`${authorData.f} ${authorData.o[0]}.${authorData.i[0]}.`}</option>
                    )}
                </SelectLabel>

                <SelectLabel
                    id="book-search-panel-search-form-jahnre-input"
                    name="jahnreId"
                    labelText="Жанр:"
                    placeHolderText="Выберите жанр"
                    state={bookGenreId}
                    setState={inputGenre}
                >
                    {genreList.map((genreData) => 
                        <option value={genreData.id} key={`genre-option-${genreData.id}`}>{genreData.name}</option>
                    )}
                </SelectLabel>

                <InputLabel
                    id="book-search-panel-search-form-min-price-input"
                    name="minPrice"
                    inputType="text"
                    inputMaxLength={12}
                    labelText={"Минимальная цена: " + bookMinPriceIncorrectReason}
                    hasError={bookMinPriceIncorrectValue}
                    state={bookMinPrice}
                    setState={inputMinPrice}
                />

                <InputLabel
                    id="book-search-panel-search-form-max-price-input"
                    name="minPrice"
                    inputType="text"
                    inputMaxLength={12}
                    labelText={"Максимальная цена: " + bookMaxPriceIncorrectReason}
                    hasError={bookMaxPriceIncorrectValue}
                    state={bookMaxPrice}
                    setState={inputMaxPrice}
                />

                <div className="books-search-panel-form-button-block">
                    <BrownButton type="submit">Найти</BrownButton>
                    <WhiteButton type="button" onClick={closeSearchWindow}>Назад</WhiteButton>
                </div>

            </form> 
            
        </div>
    )
};

export default BookSearchPanel;