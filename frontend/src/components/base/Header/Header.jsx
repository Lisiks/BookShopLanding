import { Link } from "react-router";

import "./styles.css"

const Header = (props) => {
    const {pageName} = props;

    return (
        <header className="header-block">
            <div>
                <h1>Книжный мир</h1>
                <p>{pageName}</p>
            </div>
            
            <nav>
                <Link to="/">Каталог</Link>
                <Link to="/profile">Профиль</Link>
                <Link to="/cart">Корзина</Link>
            </nav>
        </header>
    );
};


export default Header;