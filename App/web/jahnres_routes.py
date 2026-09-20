from fastapi import APIRouter, Depends, Path, Query, status, Form
from typing import Annotated

from ..services.jahnres_service import JahnreService, get_service
from ..services.auth_service import auth_admin
from ..models.jahnres_models import JahnreGetModel, JahnrePostModel
from ..models.search_and_pagination_models import JahnresSearchModel

router = APIRouter(prefix="/jahnres", tags=["✒️ jahnres"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_jahnre(
    jahnre_params: Annotated[JahnrePostModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[JahnreService, Depends(get_service)]
) -> dict[str, str]:
    await service.create_jahnre(jahnre_params)
    return {"msg": "created"}


@router.delete("/delete/{jahnre_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def delete_jahnre(
    jahnre_id: Annotated[int, Path(gt=0)],
    service: Annotated[JahnreService, Depends(get_service)]
) -> dict[str, str]:
    await service.delete_jahnre(jahnre_id)
    return {"msg": "deleted"}


@router.patch("/modify/{jahnre_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def modify_janhre(
    jahnre_params: Annotated[JahnrePostModel, Form(media_type="application/x-www-form-urlencoded")],
    jahnre_id: Annotated[int, Path(gt=0)],
    service: Annotated[JahnreService, Depends(get_service)]
) -> dict[str, str]:
    await service.modify_jahnre(jahnre_id, jahnre_params)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, JahnreGetModel])
async def get_all(
    search_params: Annotated[JahnresSearchModel, Query()],
    service: Annotated[JahnreService, Depends(get_service)]
) -> dict[int, JahnreGetModel]:
    return await service.get_all(search_params)