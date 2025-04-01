from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from module.formatear_datos.formatear_datos import convertir_a_numero_estimado

def bancoDavivienda(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://www.davivienda.com/wps/portal/personas/nuevo/personas/portlet/simulador_cdt_cobis/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_TwsTQy9LYz83P18HQ0CXf0cXQzc3Q38A0z0w8EKjC0CTfy8nIx8g_3D3AwcfV38Tb1MvI29nUz1o0jT72ZpDNRvEOzsaOlv6O9uRJx-AxzA0YA4_XgUROE3Plw_CqwEXwigKcD0Ij4FBm7mUAV4XFGQGxoaGmGQ6ZmuqAgAWONlcQ!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/")
        time.sleep(1)
    except Exception as e:
        print(f"Error al abrir la URL: {e}")
        return None

    try:
        # Esperar a que el select esté visible y se pueda hacer clic
        select_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/section/div[3]/form/div/div[2]/div/div[2]/div[2]/div/select"))
        )

        # Hacer clic en el select para desplegar las opciones
        select_element.click()

        time.sleep(2)

        # Usar ActionChains para simular las teclas de flecha hacia abajo y Enter
        actions = ActionChains(driver)
        
        # Simular la tecla hacia abajo (↓) para ir a la siguiente opción
        actions.send_keys(Keys.ARROW_DOWN)  # Flecha hacia abajo

        time.sleep(2)

        # Simular la tecla Enter para seleccionar la opción actual
        actions.send_keys(Keys.ENTER)

        time.sleep(2)

        # Ejecutar las acciones
        actions.perform()

        print("Opción seleccionada correctamente.")
        
    except Exception as e:
        print(f"Error al seleccionar la tasa fija con el teclado: {e}")
    
    time.sleep(4)

    try:
        # Esperar a que el campo de monto esté visible y hacer clic para enfocarlo
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'input_viewns_Z7_NH941K82NGNMA0QENAD0GG0OP5_:j_id_6:j_id_s'))
        )
        
        # Hacer clic para enfocar el campo de monto
        input_element.click()
        
        # Limpiar el campo por si tiene algún valor previo
        input_element.clear()

        # Ingresar el monto tecla por tecla con una pausa de 0.5 segundos
        for digit in str(amount):  # Recorrer cada dígito del monto
            input_element.send_keys(digit)  # Ingresar el dígito
            time.sleep(0.5)  # Pausar 0.5 segundos entre cada tecla

        # Simular el evento de perder el foco (blur) usando TAB
        input_element.send_keys(Keys.TAB)

        print(f"Monto insertado correctamente: {amount}")

    except Exception as e:
        print(f"Error al insertar el monto: {e}")

    time.sleep(4)

    try:
        # Esperar a que el radio button esté visible y clickeable
        radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='simuladorCobisBean_tipoPlazo']"))
        )
        
        # Ejecutar un clic utilizando JavaScript, ya que el radio button se maneja con un trigger('click')
        driver.execute_script("arguments[0].click();", radio_button)

        # Esperar 2 segundos antes de hacer el segundo clic (simulando doble clic)
        time.sleep(2)

        # Ejecutar el segundo clic
        driver.execute_script("arguments[0].click();", radio_button)
            
    except Exception as e:
        print(f"Error al simular el doble clic: {e}")


    time.sleep(4)

    try:
        # Esperar a que el campo de días esté visible y hacer clic para enfocarlo
        input_element_fecha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'input_viewns_Z7_NH941K82NGNMA0QENAD0GG0OP5_:j_id_6:j_id_1e'))
        )

        # Hacer clic para enfocar el campo de días
        input_element_fecha.click()

        # Limpiar el campo por si tiene algún valor previo
        input_element_fecha.clear()

        # Ingresar los días tecla por tecla con una pausa de 0.5 segundos
        for digit in str(days):  # Recorrer cada dígito de los días
            input_element_fecha.send_keys(digit)  # Ingresar el dígito
            time.sleep(0.5)  # Pausar 0.5 segundos entre cada tecla

        # Simular el evento de perder el foco (blur) usando TAB
        input_element_fecha.send_keys(Keys.TAB)

    except Exception as e:
        print(f"Error al insertar los días: {e}")
        return None

    time.sleep(4)

    try:
        # Localizar el select de vencimiento de pago usando su id
        select_element_vencimiento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'viewns_Z7_NH941K82NGNMA0QENAD0GG0OP5_:j_id_6:listaPeriodoInner'))
        )
        
        # Hacer clic para enfocar el select
        select_element_vencimiento.click()

        time.sleep(2)

        # Usar ActionChains para simular las teclas de flecha hacia abajo y Enter
        actions = ActionChains(driver)

        # Simular la tecla hacia abajo (↓) para seleccionar la siguiente opción
        actions.send_keys(Keys.ARROW_DOWN)

        time.sleep(2)

        # Simular la tecla Enter para confirmar la selección
        actions.send_keys(Keys.ENTER)

        time.sleep(2)

        # Ejecutar las acciones
        actions.perform()
        
    except Exception as e:
        print(f"Error al seleccionar el vencimiento de pago al final: {e}")
        return None

    time.sleep(4)

    try:
        # Localizar el botón de simular usando su id
        button_simular = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'viewns_Z7_NH941K82NGNMA0QENAD0GG0OP5_:j_id_6:btnSimular'))
        )
        
        # Esperar a que el botón esté habilitado (no deshabilitado)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'viewns_Z7_NH941K82NGNMA0QENAD0GG0OP5_:j_id_6:btnSimular'))
        )

        # Hacer clic en el botón de simular
        button_simular.click()

        time.sleep(4)

        # Hacer clic en el botón de simular
        button_simular.click()

        time.sleep(4)


        print("Botón 'Simular' clickeado correctamente.")

    except Exception as e:
        print(f"Error al dar clic al botón de simular: {e}")

    time.sleep(1)

    try:
        # Esperar a que el elemento de la ganancia estimada esté presente
        rendimientos_estimados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/section/div[3]/form/div/div/div[3]/div/table/tbody/tr[2]/td[2]/span"))
        )
        # Obtener el texto de la ganancia estimada
        rendimientos_estimados = rendimientos_estimados.text
        
        # Esperar a que el elemento de la tasa de interés esté presente
        tasa_interes = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/section/div[3]/form/div/div/div[3]/div/table/tbody/tr[3]/td[2]/span"))
        )
        # Obtener el texto de la tasa de interés
        tasa_interes = tasa_interes.text
    
    except:
        return None
    
    try:
        inversion = convertir_a_numero_estimado(amount) 
        rendimientos_estimados = convertir_a_numero_estimado(rendimientos_estimados) 
        total_ganancia = inversion + rendimientos_estimados
        
        datos_inversion = {
            'banco': "Davivienda",
            'montoInvertido': amount,
            'plazoDias': f"{days}",
            'tasaEfectivaAnual': tasa_interes,
            'rendimientosEstimados': f"{rendimientos_estimados:,.0f}",
            'retefuente': "N/A",
            'totalRecibidoAlVencimiento': f"${total_ganancia:,.0f}"
        }

        total = datos_inversion['totalRecibidoAlVencimiento']
        datos_inversion['totalRecibidoAlVencimiento'] = total.replace(",", ".")
        rendimientos = datos_inversion['rendimientosEstimados']
        datos_inversion['rendimientosEstimados'] = rendimientos.replace(",", ".")

        return datos_inversion
    except:
        return None

    