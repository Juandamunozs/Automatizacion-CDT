from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from module.formatear_datos.formatear_datos import convertir_a_numero_estimado

def bancoFinandina(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://www.bancofinandina.com/productos/cdts/simulador-cdt")
    except Exception as e:
        print(f"No se abrió el enlace: {e}")
        return None
    
    try:
        # Esperamos hasta que el campo 'Monto_Invertir' esté presente y sea visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Monto_Invertir"))
        )

        script_input_valor = f"""
            var inputElement = document.getElementById("Monto_Invertir");
            inputElement.value = "{amount}"; 

            // Disparamos el evento de cambio para el campo "Monto_Invertir"
            var eventMonto = new Event('input', {{ bubbles: true }});
            inputElement.dispatchEvent(eventMonto);
        """
        driver.execute_script(script_input_valor)

    except Exception as e:
        print(f"Error al ingresar el monto: {e}")

    try:
        # Esperamos hasta que el campo 'Plazo_Dias' esté presente y sea visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Plazo_Dias"))
        )

        # Insertar el plazo y disparar el evento
        script_input_fecha = f"""
            // Seleccionamos el campo de entrada para los días
            var inputDias = document.getElementById("Plazo_Dias");
            inputDias.value = {days};  

            // Disparamos el evento de cambio para el campo "Plazo_Dias"
            var eventDias = new Event('input', {{ bubbles: true }});
            inputDias.dispatchEvent(eventDias);
        """
        driver.execute_script(script_input_fecha)

    except Exception as e:
        print(f"Error al ingresar el plazo de CDT: {e}")

    try:
        # Esperar hasta que el campo de Tasa E.A. esté visible y extraer el valor usando XPath
        tasa_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@ng-model="data.tasaEA_texto"]'))
        )
        tasa_interes = tasa_element.get_attribute("value")

        # Esperar hasta que el campo de Ganancia esté visible y extraer el valor usando XPath
        rendimientos_estimados_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "SIM_input-onlyread")]//input[@type="text" and not(@ng-model)]'))
        )
        rendimientos_estimados = rendimientos_estimados_element.get_attribute("value")

        total_inversion_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/main/section[2]/section[2]/div[4]/div/input'))
        )
        totalRecibidoAlVencimiento = total_inversion_element.get_attribute("value")

        info_retefuente_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/main/section[2]/section[2]/div[3]/div[2]/span'))
        )
        
        info_texto = info_retefuente_element.text
        
        match = re.search(r"retenciones del (\d+,\d+|\d+)%", info_texto)

        if match:
            retefuente = match.group(1).replace(",", "")  

        rendimientos_estimados = convertir_a_numero_estimado(rendimientos_estimados)  
        retefuente_porcentaje = convertir_a_numero_estimado(retefuente) 
        totalRecibidoAlVencimiento = convertir_a_numero_estimado(totalRecibidoAlVencimiento) 
        rendimientos_estimados_formateado = rendimientos_estimados * (1 - retefuente_porcentaje / 100)

        retefuente = rendimientos_estimados - rendimientos_estimados_formateado

        # Almacenar los datos extraídos en un diccionario 
        datos_inversion = {
            'banco': "Banco Finandina", 
            'montoInvertido': amount,
            'plazoDias': f"{days}",
            'tasaEfectivaAnual': tasa_interes,
            'rendimientosEstimados': f"{rendimientos_estimados_formateado:,.0f}",
            'retefuente': f"{retefuente:,.0f}",  
            'totalRecibidoAlVencimiento': f"{totalRecibidoAlVencimiento:,.0f}",
        }

        total = datos_inversion['totalRecibidoAlVencimiento']
        datos_inversion['totalRecibidoAlVencimiento'] = total.replace(",", ".")

        return datos_inversion
    except Exception as e:
        print(f"Error al obtener los datos de la inversión: {e}")
        return None
