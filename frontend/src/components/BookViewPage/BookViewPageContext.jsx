import { useParams, useNavigate } from "react-router"

import { createContext, useState, useEffect, use } from "react";
import QueryManager from "../../query_manager";
import AddWindow from "../base/AddWindow/AddWindow";

export const BookViewPageContext = createContext({});

const BookViewPageContextProvider = (props) => {
    const {bookId} = useParams();

    const {children} = props;

    const [bookData, setBookData] = useState(
        {
            "title": "",
            "description": "",
            "authorId": null,
            "genreId": null,
            "pageCount": null,
            "writeYear": null,
            "price": null,
            "isbn": "",
            "id": null,
            "imageFilePath": "",
            "demoFilePath": "",
            "author": {
                "f": "",
                "i": "",
                "o": "",
                "id": null
            },
            "genre": {
                "name": "",
                "id": null
            }
        }
    )
    const [commentText, setCommentText] = useState("");
    const [commentTextIncorrectValue, setCommentTextIncorrectValue] = useState(false);
    const [commentTextIncorrectReason, setCommentTextIncorrentReason] = useState("");
    const [commentFormIsSubmit, setCommentFormIsSubmit] = useState(false);

    const [myCommentText, setMyCommentText] = useState(null);
    const [deleteCommentFormIsSubmit, setDeleteCommentFormIsSubmit] = useState(false);

    const [commentList, setCommentList] = useState([]);

    const [addWindowIsOpen, setAddWindowIsOpen] = useState(false);

    const [abortController, setAbortController] = useState(new AbortController());

    const navigate = useNavigate();

    useEffect(
        () => {
            Promise.all([
                QueryManager.getBookById(bookId, abortController.signal),
                QueryManager.getMyComment(bookId, abortController.signal),
                QueryManager.getAllComments(bookId, abortController.signal)
            ]).then(([bookResponce, myCommentResponce, allCommentResponce]) => {

                if (bookResponce.responceStatus === 404 || bookResponce.responceStatus === 422) {
                    navigate("/404")
                } else {
                    setBookData(bookResponce.responceBody)
                }

                if (myCommentResponce.responceStatus === 200 && myCommentResponce.responceBody.text !== null) {
                    setMyCommentText(myCommentResponce.responceBody.text);
                }

                const commentList = allCommentResponce.responceBody.filter((commentData) => 
                    commentData.user_id !== myCommentResponce.responceBody.user_id
                )
                setCommentList(commentList)

            });
            


            return () => {abortController.abort()}
        }, 
    []);


    const openAddWindow = () => {
        setAddWindowIsOpen(true);
    }

    const closeAddWindow = () => {
        setAddWindowIsOpen(false)
    }

    const addBook = (count) => {
        const cartData = JSON.parse(localStorage.getItem("cart")) ?? {};

        if (!(bookData.id in Object.keys(cartData))) {

            if (Object.keys(cartData).length < 10) {
                cartData[bookData.id] = count;
            } else {
                alert("В одном заказе допустимо наличие не более 10 позиций. Для изменения заказа перейдите в раздел \"Корзина\".")
            }

        } else {
            cartData[bookData.id] += Number(count);
        }

        localStorage.setItem("cart", JSON.stringify(cartData));

        setAddWindowIsOpen(false)
    }


    const inputComment = (value) => {
        setCommentText(value);
        setCommentTextIncorrectValue(false)
        setCommentTextIncorrentReason("")
    }

    const createCommentFormSubmit = (event) => {
        event.preventDefault();

        if (commentFormIsSubmit) {
            return
        }

        setCommentFormIsSubmit(true);

        if (commentText.trim().length === 0) {
            setCommentTextIncorrectValue(true)
            setCommentTextIncorrentReason("Комментарий должен содержать хотя бы один символ")
            setCommentFormIsSubmit(false);
            return;
        }

        const commentData = new FormData(event.target);

        QueryManager.createComment(commentData, bookData.id, abortController.signal).then(
            (createResponce) => {
                setCommentFormIsSubmit(false);
                if (createResponce.responceStatus === 401) {
                    alert("Для того, чтобы оставить коммантарий, необходимо пройти процедуру аутентификации. Пожалуйста, перейдите на вкладку \"Профиль\".")
                } else if (createResponce.responceStatus === 409) {
                    alert("Вы уже оставили комментарий к этой книге.")
                } else if (createResponce.responceStatus === 201) {
                    setMyCommentText(commentText);
                }
                setCommentText("")
            }
        );
    }

    const deleteCommentFormSubmit = (event) => {
        event.preventDefault()

        if (deleteCommentFormIsSubmit) {
            return;
        }

        const deleteConfirm = confirm("Вы уверены, что хотите удалить комментарий?")

        if (!deleteConfirm) {
            return
        }

        setDeleteCommentFormIsSubmit(true);

        QueryManager.deleteComment(bookData.id, abortController.signal).then(
            (deleteResponce) => {
                console.log(deleteResponce.responceBody)
                setDeleteCommentFormIsSubmit(false);
                if (deleteResponce.responceStatus === 401 || deleteResponce.responceStatus === 404 || deleteResponce.responceStatus === 401 || deleteResponce.responceStatus === 202 ) {
                    setMyCommentText(null);
                }
            }
        )

    }



    return (
        <BookViewPageContext.Provider
            value={{
                "bookData": bookData,
                "openAddWindow": openAddWindow,
                "commentText": commentText,
                "commentTextIncorrectValue": commentTextIncorrectValue,
                "commentTextIncorrectReason": commentTextIncorrectReason,
                "inputComment": inputComment,
                "createCommentFormSubmit": createCommentFormSubmit,
                "myCommentText": myCommentText,
                "deleteCommentFormSubmit": deleteCommentFormSubmit,
                "commentList": commentList
            }}
        >
            {children}
            {addWindowIsOpen && <AddWindow 
                bookPrice={bookData.price}
                bookImageUrl={bookData.imageFilePath}
                onAdd={addBook}
                onClose={closeAddWindow}
            />}
        </BookViewPageContext.Provider>
    )
}

export default BookViewPageContextProvider;