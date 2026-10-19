import { useContext } from "react";

import InputLabel from "../../../base/InputLabel/InputLabel";
import SelectLabel from "../../../base/SelectLabel/SelectLabel";
import {BookPageContext} from "../../BookPageContext";

import "./styles.css"

const BookSearchPanel = () => {
    const {authorsList, jahnreList} = useContext(BookPageContext);

    return (
        <div className="book-search-panel">
            <div>
                <h2>Поиск книг:</h2>
                <form id="books-search-pabel-form">
                    <InputLabel
                        id="book-search-panel-search-form-title-input"
                        name="bookTitle"
                        inputType="text"
                        inputMaxLength={100}
                        inputClassName="search-inp"
                        labelText="Название книги: "
                    />

                    <SelectLabel
                        id="book-search-panel-search-form-author-input"
                        name="authorId"
                        labelText="Автор:"
                        placeHolderText="Выберите автора"
                    >
                        {authorsList.map((authorData) => {
                            <option value={authorData.id} key={`author-option-${authorData.id}`}>{`${authorData.f} ${authorData.o[0]}.${authorData.i[0]}.`}</option>
                        })}
                    </SelectLabel>

                    <SelectLabel
                        id="book-search-panel-search-form-jahnre-input"
                        name="jahnreId"
                        labelText="Жанр:"
                        placeHolderText="Выберите жанр"
                    >
                        {jahnreList.map((jahnreData) => {
                            <option value={jahnreData.id} key={`jahnre-option-${jahnreData.id}`}>{jahnreData.name}</option>
                        })}
                    </SelectLabel>

                    <InputLabel
                        id="book-search-panel-search-form-min-price-input"
                        name="minPrice"
                        inputType="text"
                        inputMaxLength={12}
                        labelText="Минимальная цена: "
                    />

                    <InputLabel
                        id="book-search-panel-search-form-max-price-input"
                        name="minPrice"
                        inputType="text"
                        inputMaxLength={12}
                        labelText="Максимальная цена цена: "
                    />
                </form> 
            </div>
        </div>
    )
};

export default BookSearchPanel;