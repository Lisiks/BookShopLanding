from fastapi import APIRouter, Depends, Path, Query, status, Form
from typing import Annotated

from ..services.shop_service import ShopService, get_service
from ..services.auth_service import auth_admin
from ..models.shops_models import ShopGetModel, ShopPostModel
from ..models.search_and_pagination_models import ShopSearchModel

router = APIRouter(prefix="/shops", tags=["🏨 shops"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_shop(
    shop_params: Annotated[ShopPostModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[ShopService, Depends(get_service)]
) -> dict[str, str]:
    await service.create_shop(shop_params)
    return {"msg": "created"}


@router.delete("/{shop_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def delete_shop(
    shop_id: Annotated[int, Path(gt=0)],
    service: Annotated[ShopService, Depends(get_service)]
) -> dict[str, str]:
    await service.delete_shop(shop_id)
    return {"msg": "deleted"}


@router.patch("/{shop_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def modify_shop(
    shop_params: Annotated[ShopPostModel, Form(media_type="application/x-www-form-urlencoded")],
    shop_id: Annotated[int, Path(gt=0)],
    service: Annotated[ShopService, Depends(get_service)]
) -> dict[str, str]:
    await service.modify_shop(shop_id, shop_params)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, ShopGetModel])
async def get_all(
    search_params: Annotated[ShopSearchModel, Query()],
    service: Annotated[ShopService, Depends(get_service)]
) -> dict[int, ShopGetModel]:
    return await service.get_all(search_params)