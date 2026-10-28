import { useContext } from "react";

import BrownButton from "../../../base/BrownButton/BrownButton";
import { BookViewPageContext } from "../../BookViewPageContext";

import "./styles.css"

const API_ORIGIN = "http://localhost:8000";

const BookInfo = () => {
    const {bookData, openAddWindow} = useContext(BookViewPageContext);

    return (

        <div className="book-view-page-container">
        
            

            <div className="book-view-page-container-info">
                <div>
                    <h2 className="book-view-page-h2">Описание:</h2>
                    <p className="book-view-page-p">{bookData.description}</p>
                    <h3 className="book-view-page-h3 margin-top-18">Автор:</h3>
                    <p className="book-view-page-p">{bookData.author.f} {bookData.author.i} {bookData.author.o}</p>
                    <h3 className="book-view-page-h3 margin-top-18">Жанр:</h3>
                    <p className="book-view-page-p">{bookData.genre.name}</p>

                    <div className="book-view-page-container-info-price margin-top-18">
                        <h3 className="book-view-page-h3">Цена: {(bookData.price)?.toFixed(2)} руб.</h3>
                        <BrownButton type="button" onClick={openAddWindow}> </BrownButton>
                    </div>
                </div>

                <img src={`${API_ORIGIN}/${bookData.imageFilePath}`} alt="Фотография обложки книги"/>
            </div>
        

        
                    
            <h2 className="book-view-page-h2">Подробности:</h2>
            <p className="book-view-page-p">Год написания: {bookData.writeYear} г.</p>
            <p className="book-view-page-p">Кол-во страниц: {bookData.pageCount} с.</p>
            <p className="book-view-page-p">ISBN: {bookData.isbn}</p>
            <p className="book-view-page-p">Демо версия: <a href={`${API_ORIGIN}/${bookData.demoFilePath}`}>Скачать</a></p>
        

        </div>
    );
};

export default BookInfo;