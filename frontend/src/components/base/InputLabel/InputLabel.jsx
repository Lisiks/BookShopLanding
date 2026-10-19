import { useState } from "react"

import "./styles.css"

const InputLabel = (props) => {
    const {id, name, inputType, inputMaxLength, inputClassName, labelText, labelErrorText, labelClassName, placeholderText, state, setState, hasError} = props;

    const [errorState, setErrorState] = useState(hasError !== null ? hasError : false);

    return (
        <div className="input-label" haserror={String(errorState)}>
            <label htmlFor={id} className={labelClassName} >{hasError === true ? labelErrorText : labelText}</label>
            <input 
                type={inputType} 
                id={id} name={name} 
                maxLength={inputMaxLength} 
                placeholder={placeholderText} 
                value={state} 
                className={inputClassName}

                onFocus={() => {setErrorState(false)}}
                onInput={(event) => {setState(event.target.value)}}
            />
        </div>
    )
    
};

export default InputLabel;