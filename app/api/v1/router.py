from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, leads_narela, logs_servicios

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    logs_servicios.router,
    prefix="/logs-servicios",
    tags=["logs-servicios"],
)
api_router.include_router(
    leads_narela.router,
    prefix="/leads-narela",
    tags=["leads-narela"],
)
