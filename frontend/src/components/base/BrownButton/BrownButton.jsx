import "./styles.css"

const BrownButton = (props) => {
    const {type, onClick, children, className} = props;

    return (
        <button type={type} onClick={onClick} className={className ? `brown-btn ${className}` : "brown-btn"} >{children}</button>
    );

};

export default BrownButton;