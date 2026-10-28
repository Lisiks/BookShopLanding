import { useContext } from "react";

import TextareaLabel from "../../../base/TextareaLabel/TextareaLabel";
import BrownButton from "../../../base/BrownButton/BrownButton";
import { BookViewPageContext } from "../../BookViewPageContext";

import "./styles.css"



const CommentForm = () => {
    const {commentText, commentTextIncorrectValue, commentTextIncorrectReason, inputComment, createCommentFormSubmit} = useContext(BookViewPageContext)

    return (
        <form className="book-view-page-container-comment-form" onSubmit={createCommentFormSubmit}>
            <TextareaLabel
                id="book-page-container-comment-form-comment-textarea"
                name="text"
                textareaMaxLength={1000}
                labelText={"Оставить комментарий: " + commentTextIncorrectReason}
                hasError={commentTextIncorrectValue}
                state={commentText}
                setState={inputComment}
            />
        
            <BrownButton type="submit">Сохранить</BrownButton>
        </form>
    )
}

export default CommentForm;