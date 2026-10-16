from fastapi import Request, Response
from typing import Callable, Any, Optional, Tuple, Dict
import hashlib



def default_search_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    jahnre_search_params = kwargs["search_params"]

    cache_key = hashlib.md5( 
        f"{func.__module__}:{func.__name__}:{jahnre_search_params.model_dump_json()}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"




def books_page_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    book_id = kwargs["book_id"]

    cache_key = hashlib.md5(  
        f"{func.__module__}:{func.__name__}".encode()
    ).hexdigest()
    return f"{namespace}-{book_id}:{cache_key}"



def comments_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    book_id = kwargs["book_id"]

    cache_key = hashlib.md5( 
        f"{func.__module__}:{func.__name__}".encode()
    ).hexdigest()
    return f"{namespace}-{book_id}:{cache_key}"


def user_comment_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    book_id = kwargs["book_id"]
    user_id = kwargs["user_data"].id

    cache_key = hashlib.md5( 
        f"{func.__module__}:{func.__name__}".encode()
    ).hexdigest()
    return f"{namespace}-{book_id}-{user_id}:{cache_key}"





def user_orders_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    jahnre_search_params = kwargs["search_params"]
    user_id = kwargs["user_data"].id

    cache_key = hashlib.md5( 
        f"{func.__module__}:{func.__name__}:{jahnre_search_params.model_dump_json()}".encode()
    ).hexdigest()
    return f"{namespace}-{user_id}:{cache_key}"
