import { useContext } from "react";

import SelectLabel from "../../../base/SelectLabel/SelectLabel";
import BrownButton from "../../../base/BrownButton/BrownButton";
import WhiteButton from "../../../base/WhiteButton/WhiteButton";

import { CartPageContext } from "../../CartPageContext";

import "./styles.css"


const CreateForm = () => {
    const {shopsList, clearCart, shopId, shopIdIncorrectValue, shopIdIncorrectReason, inputShopId, createOrderFormSubmit} = useContext(CartPageContext);

    return (
        <form className="cart-page-create-order-form" onSubmit={createOrderFormSubmit}>
            <SelectLabel
                id="cart-page-shop-select-label"
                name="shopId"
                labelText={"Магазин: " + shopIdIncorrectReason}
                placeHolderText="Выберите магазин для заказа"
                state={shopId}
                setState={inputShopId}
                hasError={shopIdIncorrectValue}
            >
                {shopsList.map((shopData) => 
                    <option value={shopData.id} key={`shop-option-${shopData.id}`}>г. {shopData.town}, ул. {shopData.street}, д. {shopData.housing}</option>
                )}
            </SelectLabel>

            <div className="cart-page-create-order-from-buttons-block">
                <BrownButton type="submit">Создать заказ</BrownButton>
                <WhiteButton type="button" onClick={clearCart}>Очистить корзину</WhiteButton>
            </div>
        </form>
    )
}

export default CreateForm;