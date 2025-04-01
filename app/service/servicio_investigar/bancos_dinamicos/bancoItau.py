from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def bancoItau(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://banco.itau.co/web/personas/inversiones/cdt-virtual")
    except Exception as e:
        print(f"Error al abrir el enlace: {e}")
        return None

    try:
        # Esperar a que el iframe esté presente
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "_com_liferay_iframe_web_portlet_IFramePortlet_INSTANCE_yawq_iframe"))
        )

        # Obtener la ubicación del iframe
        iframe_location = iframe.location
        y_position = iframe_location['y']

        # Usar JavaScript para hacer scroll a la posición del iframe
        driver.execute_script(f"window.scrollTo(0, {y_position});")

        # Cambiar al iframe
        driver.switch_to.frame(iframe)
        print("Iframe cargado y desplazado correctamente")

    except Exception as e:
        print(f"Error al encontrar o hacer scroll al iframe: {e}")
        return None

    # Insertar el monto en el primer campo de entrada
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "voxel-input-0"))
        )
        input_field.clear()
        input_field.send_keys(amount)
    except Exception as e:
        print(f"Error al insertar el monto: {e}")

    # Insertar los días en el segundo campo de entrada
    try:
        input_field_1 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "voxel-input-1"))
        )
        input_field_1.clear()
        input_field_1.send_keys(days)
    except Exception as e:
        print(f"Error al insertar los días: {e}")

    time.sleep(4)

    # Buscar el botón "Simular" con el XPath proporcionado y hacer clic en él
    try:
        # Usar el XPath proporcionado para encontrar el botón "Simular"
        simular_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/main/app-cdt/div/div/form/div/div[1]/button"))
        )
        # Usar ActionChains para asegurarnos de que el clic sea ejecutado correctamente
        actions = ActionChains(driver)
        actions.move_to_element(simular_button).click().perform()
        print("¡Botón 'Simular' clickeado con éxito!")
    except Exception as e:
        print(f"Error al hacer clic en el botón 'Simular': {e}")

    try:
        # Esperar a que el botón sea clickeable
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "voxel-accordion-0"))
        )
        # Hacer clic en el botón
        button.click()
        print("¡Botón de detalles de inversión clickeado con éxito!")
    except Exception as e:
        print(f"Error al hacer clic en el botón: {e}")

    try:
        # Esperar a que el elemento con los rendimientos estimados esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'result-card--title-value')]"))
        )
    
        # Extraer los valores de los elementos con las XPaths proporcionadas
        rendimientos_estimados_str = driver.find_element(By.XPATH, "//p[contains(@class, 'result-card--title-value')]").text
        retefuente_str = driver.find_element(By.XPATH, "//voxel-list-text-detail[contains(@class, 'list-detail voxel-list-text-detail')]").text
        tasa_efectiva_anual_str = driver.find_element(By.XPATH, "//voxel-list-text-detail[contains(text(), ' %')]").text
        monto_invertido_str = driver.find_element(By.XPATH, "//voxel-list-text-detail[contains(@class, 'list-detail voxel-list-text-detail') and contains(text(), '$')]").text
        total_recibido_al_vencimiento_str = driver.find_element(By.XPATH, "//p[contains(@class, 'result-card--p')]").text

        # Construir el diccionario con los datos sin limpiarlos
        datos_inversion = {
            'banco': "Itaú", 
            'montoInvertido': monto_invertido_str,
            'plazoDias': f"{days}",
            'tasaEfectivaAnual': tasa_efectiva_anual_str,
            'rendimientosEstimados': rendimientos_estimados_str,
            'retefuente': retefuente_str,
            'totalRecibidoAlVencimiento': total_recibido_al_vencimiento_str
        }

        # Volver al contenido principal fuera del iframe
        driver.switch_to.default_content()

        if datos_inversion['totalRecibidoAlVencimiento'] == "$ 0":
            return None
        
        return datos_inversion
    except Exception as e:
        print(f"Error al extraer los datos: {e}")
        return None