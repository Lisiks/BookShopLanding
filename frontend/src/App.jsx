import {Routes, Route} from "react-router"


import BookPage from "./components/BookPage/BookPage.jsx"
import ProfilePage from "./components/ProfilePage/ProfilePage.jsx"
import CartPage from "./components/CartPage/CartPage.jsx"
import LoginPage from "./components/LoginPage/LoginPage.jsx"
import RegisterPage from "./components/RegisterPage/RegisterPage.jsx"
import BookViewPage from "./components/BookViewPage/BookViewPage.jsx"
import ErrorPage from "./components/ErrorPage/ErrorPage.jsx"
import GlobalBookContextPrivoder from "./GlobalBookContextProvider.jsx"

import "./styles/fonts.css"
import "./styles/vars.css"
import "./styles/app.css"

const App = () => {
    return (
        <GlobalBookContextPrivoder>
            <Routes>
                <Route path="/" element={<BookPage/>}/>
                <Route path="/books" element={<BookPage/>}/>
                <Route path="/books/:bookId" element={<BookViewPage/>}/>

                <Route path="/profile" element={<ProfilePage/>}/>
                <Route path="/cart" element={<CartPage/>}/>
                <Route path="/login" element={<LoginPage/>}/>
                <Route path="/register" element={<RegisterPage/>}/>
                <Route path="*" element={<ErrorPage/>}/>
            </Routes>
        </GlobalBookContextPrivoder>
    )
}

export default App
