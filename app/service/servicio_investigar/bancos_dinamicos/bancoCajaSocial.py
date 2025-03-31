from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from module.formatear_datos.formatear_datos import convertir_a_numero_estimado
import time

def bancoCajaSocial(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://simuladores.bancocajasocial.net/SimuladoresRWD/Certificados")
    except:
        print("No se abrió el enlace")
        return None

    time.sleep(1)

    # Ejecutar JS para seleccionar "CDT_TF_INTERESUNICO" en el <select> y actualizar la interfaz
    driver.execute_script("""
        const selectElement = document.getElementById('cbmTipoCDT');
        selectElement.value = "CDT_TF_INTERESUNICO";  // Selecciona "CDT Tasa fija"
        
        // Actualizar la interfaz personalizada del select
        const styledSelect = document.querySelector('.styledSelect');
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        styledSelect.innerText = selectedOption.text;
        
        // Disparar el evento 'change' para actualizar la interfaz
        selectElement.dispatchEvent(new Event('change'));
    """)

    time.sleep(1)

    # Insertar el monto de depósito en el input "txtValorCredito"
    input_valor_credito = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'txtValorCredito'))
    )
    input_valor_credito.send_keys(str(amount))  # Insertar el valor del depósito
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", input_valor_credito)  # Disparar el evento 'input'

    time.sleep(1)

    # Insertar el plazo en días en el input "txtPlazo"
    input_plazo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'txtPlazo'))
    )
    input_plazo.send_keys(str(days))  # Insertar el valor del plazo en días
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", input_plazo)  # Disparar el evento 'input'

    # Esperar a que el botón 'Simular' esté habilitado y hacer clic
    btn_simular = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'btnSimular'))
    )

    # Asegurarse de que el botón esté habilitado antes de hacer clic
    if btn_simular.is_enabled():
        btn_simular.click()  # Hacer clic en el botón
    else:
        print("El botón 'Simular' está deshabilitado.")

    time.sleep(3)

    script_extraer_datos = f"""
            let inversion = {{
                banco: "Banco Caja Social", // Nombre del banco (en este caso es Banco Caja Social)
                montoInvertido: "0", // Monto invertido (en este caso 9,500,000 como string)
                plazoDias: document.querySelector("#txtPlazo").value, // Extraer el valor del input con id "txtPlazo" (plazo en días)
                tasaEfectivaAnual: document.querySelector("#TasaInteres").value + "%", // Extraer la tasa de interés desde el input con id "TasaInteres"
                // Extraer rendimientos estimados del elemento con id "RendimientoTotal" y limpiar los caracteres no numéricos
                rendimientosEstimados: document.querySelector("#RendimientoTotal").innerText.replace(/[^\d,]/g, '').replace(',', ''),
                // Extraer la retención en la fuente del elemento con id "RetencionFuente" y limpiar los caracteres no numéricos
                retefuente: document.querySelector("#RetencionFuente").innerText.replace(/[^\d,]/g, '').replace(',', ''),
                // Total recibido al vencimiento (dejar en blanco como se indicó)
                totalRecibidoAlVencimiento: ""
            }};

            inversion.totalRecibidoAlVencimiento = "";
            return inversion;  // Retorna el objeto inversion con los datos extraídos
        """
    datos_inversion = driver.execute_script(script_extraer_datos)

    rendimientos_estimados = convertir_a_numero_estimado(datos_inversion['rendimientosEstimados'])  
    total_Recibido_Al_Vencimiento = convertir_a_numero_estimado(amount) 

    total_ganancia = rendimientos_estimados + total_Recibido_Al_Vencimiento
    datos_inversion = {
        'banco': datos_inversion['banco'],
        'montoInvertido': amount,
        'plazoDias': datos_inversion['plazoDias'],
        'tasaEfectivaAnual': datos_inversion['tasaEfectivaAnual'],
        'rendimientosEstimados': datos_inversion['rendimientosEstimados'],
        'retefuente': datos_inversion['retefuente'],
        'totalRecibidoAlVencimiento': f"${total_ganancia:,.0f}"
    }

    if datos_inversion['totalRecibidoAlVencimiento'] == "":
        return None
    else:
       total = datos_inversion['totalRecibidoAlVencimiento']
       datos_inversion['totalRecibidoAlVencimiento'] = total.replace(",", ".")
       
    return datos_inversion