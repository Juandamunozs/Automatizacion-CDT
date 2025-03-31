from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from module.time.time import calcular_fecha_futura
import time

def bancoBogota(days, amount, email, driver):
    try:
        # Acceder a la URL
        driver.get("https://cdtdigital.bancodebogota.com.co/index.html?utm_source=google&utm_medium=search&utm_campaign=cdt-cdt-col-gg-sr-br-ccn-cdt_aon_bcg_open_search_google_nov_2024&utm_content=search&utm_term=cdt_aon_bcg_open_search_google_nov_2024&gad_source=1&gclid=CjwKCAjw7pO_BhAlEiwA4pMQvMUUcfL8ZLVFQKXnllOSsQDAwysbVuQ-A8uem7VIIhKt8DqIfav5zBoC-VMQAvD_BwE")
    except:
        print("No se abrio el enlace")
        return None

    try:
        script_scrool = f"""
            // Seleccionamos el elemento con la clase 'simulator__title'
            const title = document.querySelector('.simulator__title');

            // Hacemos scroll hacia el elemento
            title.scrollIntoView({{
            behavior: 'smooth', 
            block: 'start'      
            }});

            """
        driver.execute_script(script_scrool)
    except:
        print(f"Error al hacer el scroll")


    try:
        # Esperar a que el componente bdb-at-input esté disponible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "bdb-at-input"))
        )

        # Insertar el valor en el campo de cantidad
        script_input_valor = f"""
        (function insertAmount(amount) {{
            // Seleccionar el componente web 'bdb-at-input'
            const webComponent = document.querySelector("bdb-at-input");

            if (!webComponent) {{
                console.error("❌ El componente 'bdb-at-input' no fue encontrado.");
                return;
            }}

            // Verificar si el componente tiene shadowRoot
            const shadowRoot = webComponent.shadowRoot;
            if (!shadowRoot) {{
                console.error("❌ El componente 'bdb-at-input' no tiene shadowRoot.");
                return;
            }}

            // Seleccionar el campo de entrada dentro del shadowRoot
            const input = shadowRoot.querySelector("input");

            if (!input) {{
                console.error("❌ No se encontró el campo de entrada en el shadowRoot.");
                return;
            }}

            // Establecer el valor del input (monto)
            input.value = amount;

            // Crear un evento 'input' para simular la interacción del usuario
            const inputEvent = new Event("input", {{ bubbles: true }});

            // Disparar el evento para actualizar el valor
            input.dispatchEvent(inputEvent);

            console.log(`💰 Monto establecido: ${amount}`);
        }})("{amount}");
        """

        # Ejecutar el script con el driver de Selenium
        driver.execute_script(script_input_valor)
    except Exception as e:
        print("Error al insertar el valor:", e)


    fecha = calcular_fecha_futura(days)

    try:
        # Esperar a que el componente bdb-ml-calendar-lite esté disponible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "bdb-ml-calendar-lite"))
        )

        # Insertar la fecha en el campo de fecha
        script_input_fecha = f"""
        (function setCalendarDate(dateString) {{
            let webComponent = document.querySelector("bdb-ml-calendar-lite");

            if (webComponent && webComponent.shadowRoot) {{
                let inputComponent = webComponent.shadowRoot.querySelector("#bdb-ml-calendar-lite__input");

                if (inputComponent && inputComponent.shadowRoot) {{
                    let input = inputComponent.shadowRoot.querySelector(".input-box__content__input");
                    
                    if (input) {{
                        input.value = dateString;  
                        input.dispatchEvent(new Event("input", {{ bubbles: true }})); 
                        console.log("📅 Fecha establecida:", dateString);
                    }} else {{
                        console.log("❌ No se encontró el input con la clase 'input-box__content__input'.");
                    }}
                }} else {{
                    console.log("❌ `bdb-ml-calendar-lite__input` no tiene ShadowRoot o no se encontró.");
                }}
            }} else {{
                console.log("❌ No se encontró el componente `bdb-ml-calendar-lite` o no tiene ShadowRoot.");
            }}
        }})("{fecha}"); 
        """
        driver.execute_script(script_input_fecha)
    except Exception as e:
        print(f"Error al insertar la fecha: {e}")

    try:
        # Esperar a que el botón esté disponible y luego hacer clic
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "simulatorButton"))
        )

        script_btn_simular = """
            let button = document.querySelector("#simulatorButton");
            if (button) {
                console.log("✅ Botón encontrado. Haciendo clic...");
                button.click();
            } else {
                console.log("❌ Botón no encontrado.");
            }
        """
        driver.execute_script(script_btn_simular)
    except:
        print(f"Error al dar click a simular inversion")

    time.sleep(2)

    # # Espera explícita para asegurar que los elementos estén cargados
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, '.simulator__resume-deadline'))
    # )

    try:
        # Obtener los datos de la inversión
        script_extraer_datos = f"""
        function obtenerTexto(selector) {{
            let elemento = document.querySelector(selector);
            return elemento ? elemento.innerText.trim() : "❌ No encontrado";
        }}

        let inversion = {{
            banco: "Banco de Bogotá",
            montoInvertido: "{amount}", 
            plazoDias: obtenerTexto(".simulator__resume-deadline.deadLine"), 
            tasaEfectivaAnual: obtenerTexto(".rate"), 
            rendimientosEstimados: obtenerTexto(".simulator__resume-income.totalIncome"), 
            retefuente: obtenerTexto(".incomeDiscount"), 
            totalRecibidoAlVencimiento: obtenerTexto(".totalPayment") 
        }};

        return inversion;
        """

        datos_inversion = driver.execute_script(script_extraer_datos)

        # Verificar si alguno de los valores es igual a las plantillas que indican que no se ha actualizado
        if (
            datos_inversion["plazoDias"] in ["{{deadLine}}", "❌ No encontrado"] or
            datos_inversion["rendimientosEstimados"] in ["{{totalIncome}}", "❌ No encontrado"] or
            datos_inversion["retefuente"] in ["{{incomeDiscount}}", "❌ No encontrado"] or
            datos_inversion["tasaEfectivaAnual"] in ["{{rate}}", "❌ No encontrado"] or
            datos_inversion["totalRecibidoAlVencimiento"] in ["{{totalPayment}}", "❌ No encontrado"]
        ):
            return None  # Si alguno de los valores no es válido, devolver None

        return datos_inversion  # Si todos los valores son válidos, devolver los datos de inversión

    except Exception as e:
        # En caso de error, devolver None
        print(f"Error al obtener los datos: {e}")
        return None
