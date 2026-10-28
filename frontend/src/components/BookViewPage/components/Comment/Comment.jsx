import "./styles.css"

const Comment = (props) => {
    const {username, date, text} = props;

    return (
        <div className="book-view-page-comment">
            <div>
                <p>{username}</p>
                <p>{date}</p>
            </div>
            <p>{text}</p>
        </div>
    );
}

export default Comment;