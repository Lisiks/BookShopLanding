import { useState, useEffect, useRef } from "react";

import BrownButton from "../BrownButton/BrownButton";

import "./styles.css"

const AddWindow = (props) => {
    const {bookPrice, bookImageUrl, onAdd, onClose} = props;

    
    const [count, setCount] = useState(1);
    const windowRef = useRef(null);


    useEffect(() => {
        const onClickCloseFunc = (event) => {
            if (event.target === windowRef.current) {
                onClose();
            }
        };

        document.addEventListener("click", onClickCloseFunc);

        return () => {
            document.removeEventListener("click", onClickCloseFunc) 
        };

    }, []);

    return (
        <div className="add-window" ref={windowRef}>
            <div>
                <img src={bookImageUrl} alt="Фотография обложки книги"/>
                <div>
                    <div>
                        <BrownButton onClick={() => {if (count > 1) {setCount(count - 1)}}}>-</BrownButton>
                        <p>{count}</p>
                        <BrownButton onClick={() => {setCount(count + 1)}}>+</BrownButton>
                    </div>
                    <p>{(bookPrice * count).toFixed(2)} руб.</p>
                </div>
                <BrownButton onClick={() => { onAdd(count) } }>Добавить</BrownButton>
            </div>
        </div>
    )
};

export default AddWindow;