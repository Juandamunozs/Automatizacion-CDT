from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from module.formatear_datos.formatear_datos import convertir_a_numero_estimado

def bancoBancolombia(days, amount, email, driver):

    try:
        # Acceder a la URL
        driver.get("https://www.bancolombia.com/personas/productos-servicios/inversiones/cdts/inversion-virtual/simulador-inversion-virtual")
    except:
        print("No se abrió el enlace")
        return None

    try:
        # Espera a que el botón 'CONTINUAR' sea visible y luego hace clic
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'boton-seleccion-tarjeta')))
        script_continuar = f"""
            document.getElementById('boton-seleccion-tarjeta').click(); 
        """
        driver.execute_script(script_continuar)
    except:
        print(f"Error al dar click al continuar")

    try:
        # Espera a que el campo de "monto" esté visible antes de insertarlo
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'valor-simulacion')))
        script_input_valor = f"""
           document.getElementById('valor-simulacion').value = '{amount}'; 

           // Forzar que Angular detecte el cambio
           const inputElement = document.getElementById('valor-simulacion');
           inputElement.dispatchEvent(new Event('input'));
        """
        driver.execute_script(script_input_valor)
    except:
        print(f"Error al ingresar el monto")

    try:
        # Espera a que el input del radio button "Sí" sea visible antes de hacer clic
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'opcion-si-input')))
        script_btn_plazo = f"""
           document.getElementById('opcion-si').click(); 
           document.getElementById('opcion-si-input').click(); 
        """
        driver.execute_script(script_btn_plazo)
    except:
        print(f"Error al dar click en plazo de cdt")

    try:
        # Espera a que el campo de "plazo" esté visible antes de insertarlo
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'valor-plazo')))
        script_input_fecha = f"""
           // Cambiar el valor del DOM
            document.getElementById('valor-plazo').value = '{days}';

            // Forzar que Angular detecte el cambio (no recomendado si usas formularios reactivos)
            const inputElement = document.getElementById('valor-plazo');
            inputElement.dispatchEvent(new Event('input'));
        """
        driver.execute_script(script_input_fecha)
    except:
        print(f"Error al ingresar el plazo de cdt")

    time.sleep(1)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'boton-simular')))
        driver.execute_script("document.getElementById('boton-simular').click();")
        print("Botón SIMULAR clickeado")
    except Exception as e:
        print(f"Error al dar clic en el botón SIMULAR: {e}")

    max_intentos = 40
    intento_actual = 0

    while intento_actual < max_intentos:
        try:
            # Espera hasta que el reCAPTCHA esté visible
            recaptcha_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "rc-imageselect"))
            )
            
            # Si encontramos el reCAPTCHA, entonces estamos atrapados en el challenge
            print("reCAPTCHA activo. Intentando de nuevo...")
            
            # Espera 1 segundo antes de intentar nuevamente
            time.sleep(1)
            
            intento_actual += 1

        except Exception as e:
            # Si no encontramos el reCAPTCHA, significa que ya hemos pasado el challenge
            print("reCAPTCHA resuelto o no presente, continuando ejecución.")
            break

        if intento_actual >= max_intentos:
            print("Número máximo de intentos alcanzado. Saliendo.")
            break

    try:
        # Aquí va el script en JavaScript que se ejecutará en el contexto del navegador
        script_extraer_datos = """
        const accordionPanels = document.querySelectorAll('mat-expansion-panel');

        // Asegurarse de que haya al menos dos paneles para poder acceder al índice [1]
        if (accordionPanels.length > 1) {
            // Seleccionar el segundo panel (índice 1)
            const secondPanel = accordionPanels[1];

            // Extraer las tasas de interés y otros datos del segundo panel
            const tasaEfectiva = secondPanel.querySelectorAll('.row.no-gutters')[0].querySelector('small').nextElementSibling.textContent.trim();
            const tasaNominal = secondPanel.querySelectorAll('.row.no-gutters')[1].querySelector('small').nextElementSibling.textContent.trim();
            const interesesAntesRetefuente = secondPanel.querySelectorAll('.row.no-gutters')[2].querySelector('small').nextElementSibling.textContent.trim();
            const retencionFuente = secondPanel.querySelectorAll('.row.no-gutters')[3].querySelector('small').nextElementSibling.textContent.trim();

            // Extraer todos los elementos que contienen los títulos de las tarjetas (por ejemplo, "240 días", "500 días", etc.)
            const cardTitles = document.querySelectorAll('.title-card');
            const times = [];
            cardTitles.forEach(card => {
                times.push(card.innerText.trim()); // Almacenamos el texto del título (que es el tiempo de inversión)
            });

            // Extraer los montos de inversión (por ejemplo, "$ 1,000,000")
            const amounts = [];
            const amountElements = document.querySelectorAll('.monto-datils h5');
            amountElements.forEach(amount => {
                amounts.push(amount.innerText.trim()); // Extraemos el valor dentro del h5
            });

            // Extraer las ganancias estimadas (por ejemplo, "$58,160", "$125,000", etc.)
            const gains = [];
            const gainElements = document.querySelectorAll('.numero-cuotas');
            gainElements.forEach(gain => {
                gains.push(gain.innerText.trim()); // Extraemos el texto de la ganancia
            });

            // Convertir los valores extraídos a números (eliminando "$" y comas)
            const montoInvertido = parseFloat(amounts[1].replace(/[^0-9.-]+/g, ""));  // Eliminar símbolos monetarios y convertir a número
            const rendimientosEstimados = parseFloat(gains[1].replace(/[^0-9.-]+/g, ""));  // Hacer lo mismo con la ganancia
            const retefuenteValor = parseFloat(retencionFuente.replace(/[^0-9.-]+/g, ""));  // Eliminar símbolos y convertir a número

            // Calcular el total recibido al vencimiento
            const totalRecibidoAlVencimiento = montoInvertido + rendimientosEstimados - retefuenteValor;

            // Generar el objeto de inversión con los datos extraídos
            let inversion = {
                banco: "Bancolombia", // Nombre del banco
                montoInvertido: amounts[1], // Monto invertido del índice [1]
                plazoDias: times[1], // Plazo de inversión (días) del índice [1]
                tasaEfectivaAnual: tasaEfectiva, // Tasa efectiva anual
                rendimientosEstimados: gains[1], // Rendimientos estimados (ganancia) del índice [1]
                retefuente: retencionFuente, // Retención en la fuente
                totalRecibidoAlVencimiento: `$${totalRecibidoAlVencimiento.toLocaleString()}` // Total recibido al vencimiento
            };

            return inversion;
        }
        """

        datos_inversion = driver.execute_script(script_extraer_datos)

        rendimientos_estimados = convertir_a_numero_estimado(datos_inversion['rendimientosEstimados'])  
        retefuente = convertir_a_numero_estimado(datos_inversion['retefuente']) 

        rendimientos_sin_retefuente = rendimientos_estimados - retefuente

        datos_inversion = {
            'banco': datos_inversion['banco'],
            'montoInvertido': datos_inversion['montoInvertido'],
            'plazoDias': datos_inversion['plazoDias'],
            'tasaEfectivaAnual': datos_inversion['tasaEfectivaAnual'],
            'rendimientosEstimados': f"${rendimientos_sin_retefuente:,.0f}",
            'retefuente': datos_inversion['retefuente'],
            'totalRecibidoAlVencimiento': datos_inversion['totalRecibidoAlVencimiento']
        }
        return datos_inversion
    except:
        return None
