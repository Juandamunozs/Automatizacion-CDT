from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def bancoFalabella(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://www.bancofalabella.com.co/falabellasimulador/cdt")
    except Exception as e:
        print(f"No se abrió el enlace: {e}")
        return None

    try:
        # Esperar que el campo "valor" esté disponible antes de ingresar el monto
        valor_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "valor"))
        )
        valor_element.clear()  # Limpiar el campo antes de ingresar el valor
        valor_element.send_keys(str(amount))  # Usar send_keys para ingresar el monto
    except Exception as e:
        print(f"Error al ingresar el valor: {e}")
        return {"error": "No se pudo ingresar el monto"}

    try:
        # Esperar que el campo "plazo" esté disponible antes de ingresar los días
        plazo_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "plazo"))
        )
        plazo_element.clear()  # Limpiar el campo antes de ingresar el plazo
        plazo_element.send_keys(str(days))  # Usar send_keys para ingresar los días
    except Exception as e:
        print(f"Error al ingresar el plazo: {e}")
        return {"error": "No se pudo ingresar el plazo"}

    try:
        # Esperar que el campo de selección de tipo CDT esté disponible
        tipo_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TipoSelect"))
        )
        tipo_select = Select(tipo_select_element)  # Usar Select para trabajar con el elemento <select>
        tipo_select.select_by_value('1')  # Seleccionar la opción de tasa fija (suponiendo que '1' es la opción correcta)
    except Exception as e:
        print(f"Error al seleccionar la tasa fija: {e}")
        return {"error": "No se pudo seleccionar la tasa fija"}

    try:
        # Esperar que el campo de periodicidad esté disponible
        periodicidad_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "periodicidadSelect"))
        )
        periodicidad_select = Select(periodicidad_select_element)  # Usar Select para trabajar con el elemento <select>
        periodicidad_select.select_by_value('6')  # Seleccionar la opción de vencimiento de pago (suponiendo que '6' es la opción correcta)
    except Exception as e:
        print(f"Error al seleccionar la fecha de pago de ganancias: {e}")
        return {"error": "No se pudo seleccionar la periodicidad"}

    try:
        # Esperar que el botón de simular esté disponible y hacer clic
        btn_simular_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "SimularCDT"))
        )
        btn_simular_element.click()  # Usar click() en lugar de execute_script
    except Exception as e:
        print(f"Error al dar clic al botón simular: {e}")
        return {"error": "No se pudo hacer clic en el botón simular"}

    # Esperar que los elementos de la simulación estén visibles
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".greenBFnumeros.ng-binding"))
    )

    # Esperar a que el valor final de la inversión esté disponible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'p[style="color: #43B02A;font-weight: 800;font-size: 30px;"]'))
    )

    time.sleep(2)


    script_extraer_datos = """
        try {
            let elementos = document.querySelectorAll('.greenBFnumeros.ng-binding');
            
            // Verificamos si los elementos necesarios están presentes
            if (elementos.length === 0) {
                console.log("No se encontraron los elementos de la inversión.");
                throw new Error('No se encontraron los elementos necesarios en la página.');
            }
            
            // Extraemos y limpiamos los datos
            let tasaEfectivaAnual = elementos[0].innerText.trim().replace('%', '').replace(/\s+/g, '');
            let rentabilidadPeriodo = elementos[2].innerText.trim().replace('$', '').replace(',', '').replace(/\s+/g, '');
            let rentabilidadNeta = elementos[3].innerText.trim().replace('$', '').replace(',', '').replace(/\s+/g, '');
            let retencionFuente = elementos[4].innerText.trim().replace('$', '').replace(',', '').replace(/\s+/g, '');
            
            // Extraemos el valor final de la inversión
            let valorFinal = document.querySelector('p[style="color: #43B02A;font-weight: 800;font-size: 30px;"]').innerText.trim().replace('$', '').replace(',', '').replace(/\s+/g, '');

            // Formateamos los valores para agregar el símbolo $ donde corresponda y % para tasaEfectivaAnual
            tasaEfectivaAnual = tasaEfectivaAnual + '%';  // Agregar porcentaje al valor de tasaEfectivaAnual
            rentabilidadNeta = "$ " + rentabilidadNeta;  // Agregar el símbolo $ sin parsear
            retencionFuente = "$ " + retencionFuente;  // Agregar el símbolo $ sin parsear
            valorFinal = "$ " + valorFinal;  // Agregar el símbolo $ sin parsear

            // Retornar los datos de la inversión sin montoInvertido ni plazoDias
            return {
                banco: "Banco Falabella",
                tasaEfectivaAnual: tasaEfectivaAnual,
                rendimientosEstimados: rentabilidadNeta,
                retefuente: retencionFuente,
                totalRecibidoAlVencimiento: valorFinal
            };
        } catch (error) {
            console.log("Error en la ejecución del script:", error.message);
            return { error: error.message };  // Retorna un objeto de error si hay problemas
        }
    """


    # Ejecutar el script de JavaScript en el contexto de la página cargada en el navegador
    datos_inversion = driver.execute_script(script_extraer_datos)

    # Verificamos si el script devolvió un error
    if 'error' in datos_inversion:
        print(f"Error al extraer los datos: {datos_inversion['error']}")
        return datos_inversion  # Devolver el error que ocurrió en el script

    # Ahora agregamos los valores de amount y days a los datos extraídos
    datos_inversion['montoInvertido'] = amount
    datos_inversion['plazoDias'] = f"{days} días"

    return datos_inversion
