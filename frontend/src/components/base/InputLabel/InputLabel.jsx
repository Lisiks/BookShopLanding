import "./styles.css"

const InputLabel = (props) => {
    const {id, name, inputType, inputMaxLength, inputClassName, labelText, labelClassName, state, setState, hasError} = props;

    return (
        <div className="input-label" haserror={String(hasError)}>
            <label htmlFor={id} className={labelClassName} >{labelText}</label>
            <input 
                type={inputType} 
                id={id} 
                name={name} 
                maxLength={inputMaxLength} 
                value={state} 
                className={inputClassName}
                onInput={(event) => {setState(event.target.value)}}
            />
        </div>
    )
    
};

export default InputLabel;