import { useContext } from "react";
import BrownButton from "../../../base/BrownButton/BrownButton";
import { BookViewPageContext } from "../../BookViewPageContext";

import "./styles.css"


const MyComment = () => {
    const {myCommentText, deleteCommentFormSubmit} = useContext(BookViewPageContext);

    return (
        <form className="book-view-page-my-comment" onSubmit={deleteCommentFormSubmit}>
            <div>
                <h2 className="book-view-page-my-comment-header">Мой комментарий:</h2>
                <BrownButton type="submit"> </BrownButton>
            </div>
            <p className="book-view-page-my-comment-text">{myCommentText}</p>
        </form>
    )
    
}

export default MyComment;