import { useState } from "react"

import "./styles.css"


const SelectLabel = (props) => {
    const {children, id, name, selectClassName, labelText, labelClassName, placeHolderText, state, setState, hasError} = props;

    return (
        <div className="select-label" haserror={String(hasError)}>
            <label htmlFor={id} className={labelClassName}>{labelText}</label>
            <select 
                id={id}
                name={name} 
                className={selectClassName} 
                value={state} 
                onInput={(event) => {setState(event.target.value)}}
            >
                <option value="">{placeHolderText}</option>
                {children}
            </select>
        </div>
    )
}

export default SelectLabel;