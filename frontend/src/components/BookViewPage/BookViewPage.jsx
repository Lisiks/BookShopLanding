import { useParams } from "react-router"

const BookViewPage = () => {
    const {bookId} = useParams();

    return (
        <h1>This is a page of book #{bookId}</h1>
    )
};

export default BookViewPage;