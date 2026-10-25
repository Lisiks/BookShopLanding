import CartPageContextProvider from "./CartPageContext"

import Header from "../base/Header/Header"
import CreateForm from "./components/CreateForm/CreateForm"
import ItemList from "./components/ItemList/ItemList"
import OrderSum from "./components/OrderSum/OrderSum"

import "./styles.css"



const CartPage = () => {
    return (
        <CartPageContextProvider>
            <main className="cart-page-main">
                <Header pageName="Корзина"/>
                <OrderSum/>
                <CreateForm/>
                <ItemList/>
            </main>
        </CartPageContextProvider>
    )
}

export default CartPage;