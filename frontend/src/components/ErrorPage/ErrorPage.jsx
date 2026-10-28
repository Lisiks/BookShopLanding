
import Header from "../base/Header/Header";


import "./styles.css"

const ErrorPage = () => {
    return (
        <>
            <title>Книжный мир: Страница не найдена</title>
            <main className="error-page-main">
                <Header pageName="Ошибка 404 - не найдено"/>
                <div className="error-page-component-info">
                    <h2>404</h2>
                    <p>Страница не найдена, возможно, данные связанные с ней были удалены или изменены.</p>
                </div>
            </main>
        </>
    )
};

export default ErrorPage;