import { useContext } from "react"

import Comment from "../Comment/Comment"

import { BookViewPageContext } from "../../BookViewPageContext"

import "./styles.css"

const CommentList = () => {
    const {commentList} = useContext(BookViewPageContext);

    return (
        <div className="book-page-container-comment-list">
            {commentList.map((commentData) => 
                
                <Comment
                    key={`comment-${commentData.user_id}`}
                    username={commentData.username}
                    text={commentData.text}
                    date={commentData.datetime.split("T")[0]}
                />
            )}
        </div>
    )
}

export default CommentList;