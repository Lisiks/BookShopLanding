import "./styles.css"

const BrownButton = (props) => {
    const {type, onClick, children} = props;

    return (
        <button type={type} onClick={onClick} className="brown-btn" >{children}</button>
    );

};

export default BrownButton;