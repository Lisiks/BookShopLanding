from fastapi import APIRouter, status, Depends
from typing import Annotated
from datetime import datetime, timezone

from ..services.healthcheck_service import HealthCheckService, get_healthcheck_service

router = APIRouter(prefix="/healthcheck", tags=["❤️ health"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[str, str])
def app_health(service: Annotated[HealthCheckService, Depends(get_healthcheck_service)]) -> dict[str, str]:
    result = service.check_app_health()
    return {
        "msg": result, 
        "datetime": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")
    }


@router.get("/redis", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def redis_health(service: Annotated[HealthCheckService, Depends(get_healthcheck_service)]) -> dict[str, str]:
    result = await service.check_redis_health()
    return {
        "msg": result, 
        "datetime": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")
    }


@router.get("/database", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def database_health(service: Annotated[HealthCheckService, Depends(get_healthcheck_service)]) -> dict[str, str]:
    result = await service.check_db_health()
    return {
        "msg": result, 
        "datetime": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")
    }