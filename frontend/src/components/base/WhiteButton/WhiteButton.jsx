import "./styles.css"

const WhiteButton = (props) => {
    const {type, onClick, children, className, hasError} = props;

    return (
        <button type={type} onClick={onClick} className={className ? `white-btn ${className}` : "white-btn"} haserror={String(hasError)}>{children}</button>
    );

};

export default WhiteButton;