from module.email.modulo_correo.email import send_email
from module.formatear_datos.formatear_datos import  ordenar_bancos_por_tasa
from module.pdf.pdfService import crear_pdf
from res.json import guardar_exito_json
from service.driver.driver import iniciar_driver
from service.servicio_investigar.investigar_tasas_bancos import investigaciones_cdt

# Función para investigar un equipo
def investigar_cdt(days, amount, email):
    try:
      driver = iniciar_driver()
    except:
       print("Error al crear driver")

    try:
        res_investigacion = investigaciones_cdt(days, amount, email, driver)

        res_investigacion = ordenar_bancos_por_tasa(res_investigacion)

        driver.quit() 

        guardar_exito_json(res_investigacion)

        crear_pdf(res_investigacion, email)
        # send_email(res_investigacion, email)

        return res_investigacion
    except Exception as e:
        driver.quit() 
        print("Error al abrir el navegador: ", e)
        return f"Error al abrir el controlador de chrome: {res_investigacion}"
    
