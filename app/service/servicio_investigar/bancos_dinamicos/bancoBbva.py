from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bancoBbva(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://www.avvillas.com.co/abrir-cdt-avvillas/?gad_source=1&gclid=Cj0KCQjw16O_BhDNARIsAC3i2GDrkLyoP4nTXS2XiwJwserdcm88c5DGY34b27u7D2Ge_epaWkn3PqQaAiSiEALw_wcB")
        
        # Esperar a que el campo de cantidad esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "adbTarget-simulator-amount")))
    except Exception as e:
        print(f"No se abrió el enlace o no se encontró el campo de cantidad: {e}")
        return None

    try:
        # Esperar que el campo para ingresar el monto esté listo antes de ejecutar el script
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "adbTarget-simulator-amount")))

        # Insertar el monto y disparar el evento
        script_input_valor = f"""
            document.getElementById("adbTarget-simulator-amount").value = "{amount}";
            var event = new Event('input');
            document.getElementById("adbTarget-simulator-amount").dispatchEvent(event);
        """
        driver.execute_script(script_input_valor)

    except Exception as e:
        print(f"Error al ingresar el monto: {e}")

    try:
        # Esperar que el campo para ingresar el plazo esté listo antes de ejecutar el script
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "adbTarget-simulator-term")))

        # Insertar el plazo y disparar el evento
        script_input_fecha = f"""
            document.getElementById("adbTarget-simulator-term").value = "{days}";
            var event = new Event('input');
            document.getElementById("adbTarget-simulator-term").dispatchEvent(event);
        """
        driver.execute_script(script_input_fecha)

    except Exception as e:
        print(f"Error al ingresar el plazo de CDT: {e}")

    try:
        # Esperar que el botón de "SIMULAR" esté disponible antes de ejecutar el script
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "adbTarget-simulate-button")))

        # Habilitar el botón y hacer clic
        script_btn_simular = """
            document.getElementById("adbTarget-simulate-button").classList.remove("adbTarget-disabled");
            document.getElementById("adbTarget-simulate-button").click();
        """
        driver.execute_script(script_btn_simular)

    except Exception as e:
        print(f"Error al dar click en simular: {e}")

    try:
        # Esperar hasta que el elemento con la clase 'adbTarget-cards-container__title' esté visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "adbTarget-cards-container__title")))

        # El script de extracción de datos en JavaScript
        script_extraer_datos = f"""
            let inversion = {{ 
                banco: "AV VILLAS", // Nombre del banco (en este caso es Avvillas según el contexto)
                montoInvertido: document.querySelector(".adbTarget-0-amount").innerText.replace(/\$|,/g, ''), // Monto invertido (como string)
                plazoDias: document.querySelector("#adbTarget-0-term").innerText.match(/\d+/)[0], // Extraer los días del plazo (como string)
                tasaEfectivaAnual: document.querySelector("#adbTarget-0-rate").innerText.match(/[\d.]+/)[0] + "%", // Extraer la tasa E.A. (como string) y agregar el porcentaje
                // Extraer rendimientos estimados, quitando el signo + y los caracteres no numéricos
                rendimientosEstimados: document.querySelector(".adbTarget-0-profit").innerText.replace(/[^\d,]/g, '').replace(',', ''), // Como string
                // Extraer la retención en la fuente y convertirlo en positivo (sin signo negativo)
                retefuente: document.querySelector(".adbTarget-0-retention").innerText.replace(/[^0-9]/g, ''), // Como string (sin signo negativo)
                // Obtener el total recibido al vencimiento desde la clase correspondiente
                totalRecibidoAlVencimiento: document.querySelector(".adbTarget-simulation-card-white-amount-text").innerText.replace(/\$|,/g, '') // Total recibido (como string)
            }};

            // No se convierte a número, se dejan como string
            inversion.montoInvertido = inversion.montoInvertido; // Se deja como string
            inversion.rendimientosEstimados = inversion.rendimientosEstimados; // Se deja como string
            inversion.retefuente = inversion.retefuente; // Se deja como string

            // Calcular el total recibido al vencimiento (en formato string también)
            let totalRecibidoAlVencimiento = `${{inversion.totalRecibidoAlVencimiento}}`;  // Solo pasamos a string
            inversion.totalRecibidoAlVencimiento = `$${{totalRecibidoAlVencimiento.toLocaleString()}}`;

            return inversion;  // Retorna el objeto inversion con los datos extraídos
        """

        # Ejecutar el script de JavaScript para extraer los datos
        datos_inversion = driver.execute_script(script_extraer_datos)

        return datos_inversion  # Retorna los datos extraídos

    except Exception as e:
        print(f"Error al traer los datos: {e}")
        return {"error": "No se pudieron obtener los datos"}

