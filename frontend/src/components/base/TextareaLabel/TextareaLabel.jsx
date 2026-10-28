import "./styles.css"

const TextareaLabel = (props) => {

    const {id, name, textareaMaxLength, textareaClassName, labelText, labelClassName, state, setState, hasError} = props;

    return (
        <div className="textarea-label" haserror={String(hasError)}>
            <label htmlFor={id} className={labelClassName} >{labelText}</label>
            <textarea 
                id={id} 
                name={name} 
                maxLength={textareaMaxLength} 
                value={state} 
                className={textareaClassName}
                onInput={(event) => { setState(event.target.value) }}
            ></textarea>
        </div>
    )
    
};


export default TextareaLabel;