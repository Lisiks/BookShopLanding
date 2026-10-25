import SelectLabel from "../../../base/SelectLabel/SelectLabel";
import BrownButton from "../../../base/BrownButton/BrownButton";
import WhiteButton from "../../../base/WhiteButton/WhiteButton";

import "./styles.css"


const CreateForm = () => {
    return (
        <form class="cart-page-create-order-form">
            <SelectLabel
                id="cart-page-shop-select-label"
                name="shopId"
                labelText="Магазин: "
                placeHolderText="Выберите магазин для заказа"
            >
                <option value="1">Киров, Ленина 34</option>
                <option value="2">Киров, Ленина 32</option>
                <option value="3">Киров, Ленина 2</option>
            </SelectLabel>

            <div class="cart-page-create-order-from-buttons-block">
                <BrownButton type="submit">Создать заказ</BrownButton>
                <WhiteButton type="button">Очистить корзину</WhiteButton>
            </div>
        </form>
    )
}

export default CreateForm;