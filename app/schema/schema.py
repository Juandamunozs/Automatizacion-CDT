from pydantic import BaseModel

# Modelo de datos para los datos de la tasa de interes
class CDTRequest(BaseModel):
    days: int
    amount: float
    email: str