import { useState } from "react"

import "./styles.css"


const SelectLabel = (props) => {
    const {children, id, name, selectClassName, labelText, labelErrorText, labelClassName, placeHolderText, state, setState, hasError} = props;

    const [errorState, setErrorState] = useState(hasError !== null ? hasError : false);

    return (
        <div className="select-label" haserror={String(errorState)}>
            <label htmlFor={id} className={labelClassName}>{hasError === true ? labelErrorText : labelText}</label>
            <select 
                name={name} 
                id={id} 
                className={selectClassName} 
                value={state} 
                onInput={(event) => {setState(event.target.value)}}
                onFocus={() => {setErrorState(false)}}
            >
                <option value="">{placeHolderText}</option>
                {children}
            </select>
        </div>
    )
}

export default SelectLabel;