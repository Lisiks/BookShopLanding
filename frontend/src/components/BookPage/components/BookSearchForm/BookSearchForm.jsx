import { useContext } from "react";

import InputLabel from "../../../base/InputLabel/InputLabel";
import { BookPageContext } from "../../BookPageContext";
import BrownButton from "../../../base/BrownButton/BrownButton";
import WhiteButton from "../../../base/WhiteButton/WhiteButton";

import "./styles.css"

const BookSearchForm = () => {
    const { openSearchWindow, bookTitle, inputTitle, submitSearchForm, subParamsIsUse, clearSearchParams, bookMaxPriceIncorrectValue, bookMinPriceIncorrectValue } = useContext(BookPageContext);

    const parametersHasError = bookMaxPriceIncorrectValue || bookMinPriceIncorrectValue;

    return (
        <form className="book-page-search-form" onSubmit={submitSearchForm}>
            <InputLabel
                id="book-page-search-form-title-input-id"
                name="bookTitle"
                inputType="text"
                inputMaxLength={100}
                inputClassName="search-inp"
                labelText="Название книги: "
                state={bookTitle}
                setState={inputTitle}
            />
            <WhiteButton type="button" className="book-page-search-form-params-btn" hasError={String(parametersHasError)} onClick={openSearchWindow}> </WhiteButton>
            {subParamsIsUse && <BrownButton type="button" onClick={clearSearchParams} className="book-page-search-form-clear-btn"> </BrownButton>}
        </form>
    );
};

export default BookSearchForm;