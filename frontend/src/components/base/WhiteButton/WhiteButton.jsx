import "./styles.css"

const WhiteButton = (props) => {
    const {type, onClick, children, className} = props;

    return (
        <button type={type} onClick={onClick} className={className ? `white-btn ${className}` : "white-btn"} >{children}</button>
    );

};

export default WhiteButton;