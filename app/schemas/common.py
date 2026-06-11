from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    database: str
    control_cuentas_login_configured: bool = False
    logs_servicios_llego_a_tiempo: bool = False
