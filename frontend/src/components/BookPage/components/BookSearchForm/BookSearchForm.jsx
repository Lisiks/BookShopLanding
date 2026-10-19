import InputLabel from "../../../base/InputLabel/InputLabel";

import "./styles.css"

const BookSearchForm = () => {
    return (
        <form id="books-search-form" className="book-page-search-form">
            <InputLabel
                id="book-page-search-form-title-input-id"
                name="bookTitle"
                inputType="text"
                inputMaxLength={100}
                inputClassName="search-inp"
                labelText="Название книги: "
            />
            
            <button type="button" className="book-page-search-form-params-btn"></button>
            <button type="button" className="book-page-search-form-clear-btn"></button>
        </form>
    );
};

export default BookSearchForm;