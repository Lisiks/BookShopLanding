import { useContext } from "react";

import { BookViewPageContext } from "../../BookViewPageContext";
import Header from "../../../base/Header/Header";
import BookInfo from "../BookInfo/BookInfo";
import CommentForm from "../CommentForm/CommentForm";
import MyComment from "../MyComment/MyComment";
import CommentList from "../CommentList/CommentList";

import "./styles.css"

const BookMain = () => {
    const {bookData, myCommentText} = useContext(BookViewPageContext);

    return (
        <>
            <title>{`Книжный мир: ${bookData.title}`}</title>
            <main className="book-view-page-main">
                <Header pageName={bookData.title }/>
                <BookInfo/>
                <CommentForm/>
                {myCommentText !== null && <MyComment/>}
                <CommentList/>
            </main>
        </>
    )
};

export default BookMain;