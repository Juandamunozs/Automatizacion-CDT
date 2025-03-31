from fastapi import APIRouter, HTTPException
from service.service import investigar_cdt
from model.model import CDTRequest
import time
from typing import Dict
from module.time.time import calcular_fecha_futura, formatear_segundos

# Crear un router para agrupar las rutas
router = APIRouter()

@router.post("/consultar_CDT", summary="Busca mejores tasas", tags=["CDT"])
def buscar_CDT(data: CDTRequest) -> Dict: 
    inicia_analisis = time.time()

    days = data.days
    amount = data.amount
    email = data.email

    try:
        document_info = investigar_cdt(days, amount, email)
    except Exception as e:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró información para los datos proporcionados: {str(e)}"
        )
    
    finaliza_analisis = time.time()
    tiempo_analisis = finaliza_analisis - inicia_analisis

    return {
        "Investigacion_bancos": document_info,
        "Fecha_vencimiento": calcular_fecha_futura(days),
        "Tiempo_de_ejecucion": formatear_segundos(tiempo_analisis)
    }
