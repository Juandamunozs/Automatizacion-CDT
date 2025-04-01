from service.servicio_investigar.bancos_dinamicos.bancoBogota import bancoBogota
from service.servicio_investigar.bancos_dinamicos.bancoBancolombia import bancoBancolombia
from service.servicio_investigar.bancos_dinamicos.bancoFalabella import bancoFalabella
from service.servicio_investigar.bancos_dinamicos.bancoDavivienda import bancoDavivienda
from service.servicio_investigar.bancos_dinamicos.bancoBbva import bancoBbva
from service.servicio_investigar.bancos_dinamicos.bancoCajaSocial import bancoCajaSocial
from service.servicio_investigar.bancos_dinamicos.bancoFinandina import bancoFinandina
from service.servicio_investigar.bancos_dinamicos.bancoItau import bancoItau
from module.formatear_datos.formatear_datos import  monto_inicial

def investigaciones_cdt(days, amount, email, driver):
        
    amount = monto_inicial(amount)

    # Número máximo de intentos
    max_intentos = 2

    # Inicialización de las variables
    res_banco_bogota = None
    res_bancolombia = None
    res_banco_falabella = None
    res_banco_davivienda = None
    res_banco_bbva = None
    res_banco_caja_social = None
    res_banco_finandina = None
    res_banco_itau = None

    # Intentar obtener los resultados de davivienda
    intentos_davivienda = 0
    while res_banco_davivienda is None and intentos_davivienda < max_intentos:
        try:
            res_banco_davivienda = bancoDavivienda(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de davivienda: {e}")
            intentos_davivienda += 1
            if intentos_davivienda < max_intentos:
                print("Reintentando...")

    # Intentar obtener los resultados de Bancolombia
    intentos_bancolombia = 0
    while res_bancolombia is None and intentos_bancolombia < max_intentos:
        try:
            res_bancolombia = bancoBancolombia(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de Bancolombia: {e}")
            intentos_bancolombia += 1
            if intentos_bancolombia < max_intentos:
                print("Reintentando...")

    # Intentar obtener los resultados del Banco de Bogotá
    intentos_banco_bogota = 0
    while res_banco_bogota is None and intentos_banco_bogota < max_intentos:
        try:
            res_banco_bogota = bancoBogota(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT del Banco de Bogotá: {e}")
            intentos_banco_bogota += 1
            if intentos_banco_bogota < max_intentos:
                print("Reintentando...")
        
    # Intentar obtener los resultados de falabella
    intentos_falabella= 0
    while res_banco_falabella is None and intentos_falabella < max_intentos:
        try:
            res_banco_falabella = bancoFalabella(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de falabella: {e}")
            intentos_falabella += 1
            if intentos_falabella < max_intentos:
                print("Reintentando...")

    #Intentar obtener los resultados de BBVA
    intentos_banco_bbva= 0
    while res_banco_bbva is None and intentos_banco_bbva< max_intentos:
        try:
            res_banco_bbva = bancoBbva(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de bbva {e}")
            intentos_banco_bbva += 1
            if intentos_banco_bbva < max_intentos:
                print("Reintentando...")

    #Intentar obtener los resultados de banco caja social
    intentos_banco_caja_social= 0
    while res_banco_caja_social is None and intentos_banco_caja_social< max_intentos:
        try:
            res_banco_caja_social = bancoCajaSocial(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de caja social {e}")
            intentos_banco_caja_social += 1
            if intentos_banco_caja_social< max_intentos:
                print("Reintentando...")

    # Intentar obtener los resultados de banco finandina
    intentos_banco_finandina = 0
    while res_banco_finandina is None and intentos_banco_finandina< max_intentos:
        try:
            res_banco_finandina = bancoFinandina(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de finandina {e}")
            intentos_banco_finandina += 1
            if intentos_banco_finandina< max_intentos:
                print("Reintentando...")

    # Intentar obtener los resultados de banco ibau
    intentos_banco_itau = 0
    while res_banco_itau is None and intentos_banco_itau< max_intentos:
        try:
            res_banco_itau= bancoItau(days, amount, email, driver)
        except Exception as e:
            print(f"Error al buscar el CDT de itau {e}")
            intentos_banco_itau += 1
            if intentos_banco_itau < max_intentos:
                print("Reintentando...")
        
    # Devolver los resultados
    res = {
        "Banco_bogota": res_banco_bogota,
        "Banco_bancolombia": res_bancolombia,
        "Banco_falabella": res_banco_falabella,
        "Banco_davivienda": res_banco_davivienda,
        "Banco_bbva": res_banco_bbva,
        "Banco_caja_social": res_banco_caja_social,
        "Banco_finandina": res_banco_finandina,
        "Banco_itau": res_banco_itau
    }

    return res