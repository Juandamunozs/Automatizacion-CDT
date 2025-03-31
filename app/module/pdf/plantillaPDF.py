from module.time.time import obtener_hora_completa, obtener_dia_texto, obtener_dia_numero, obtener_anio, obtener_mes_texto
from module.formatear_datos.formatear_datos import monto_inicial_formateado, rendimiento_formateado, tasa_anual_formateado

def cuerpo_html(res_investigacion, email):
    # Verificar si el diccionario tiene datos
    if not res_investigacion:
        return "<p>Error: No se encontraron datos de inversión.</p>"

    # Obtener fecha y hora actuales
    hora = obtener_hora_completa()
    dia_texto = obtener_dia_texto()
    dia_numero = obtener_dia_numero()
    anio_numero = obtener_anio()
    mes_texto = obtener_mes_texto()

    # Crear la fecha completa
    fecha_completa = f"{dia_texto} {dia_numero} de {mes_texto} del {anio_numero} a las {hora}"

    # Iniciar el contenido dinámico para los bancos
    bancos_html = ""
    
    for banco_key, banco_data in res_investigacion.items():
        banco = banco_data.get('banco', 'Banco Desconocido')
        monto_invertido = banco_data.get('montoInvertido', 'Desconocido')
        plazo_dias = banco_data.get('plazoDias', 'Desconocido')
        tasa_efectiva_anual = banco_data.get('tasaEfectivaAnual', 'Desconocido')
        rendimientos_estimados = banco_data.get('rendimientosEstimados', 'Desconocido')
        retefuente = banco_data.get('retefuente', 'Desconocido')
        total_recibido = banco_data.get('totalRecibidoAlVencimiento', 'Desconocido')
        
        # Limpiar y formatear los valores monetarios
        monto_invertido = monto_inicial_formateado(monto_invertido) if monto_invertido != 'Desconocido' else monto_invertido
        rendimientos_estimados = rendimiento_formateado(rendimientos_estimados) if rendimientos_estimados != 'Desconocido' else rendimientos_estimados
        retefuente = rendimiento_formateado(retefuente) if retefuente != 'Desconocido' else retefuente
        total_recibido = rendimiento_formateado(total_recibido) if total_recibido != 'Desconocido' else total_recibido
        tasa_efectiva_anual = tasa_anual_formateado(tasa_efectiva_anual) if tasa_efectiva_anual != 'Desconocido' else tasa_efectiva_anual

            # Crear una tabla para cada banco 
        bancos_html += f"""
            <h3>{banco}</h3>
            <table class="table">
                <thead>
                    <tr>
                        <th>Descripción</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Monto a invertir</td>
                        <td>{monto_invertido}</td>
                    </tr>
                    <tr>
                        <td>Días de la inversión</td>
                        <td>{plazo_dias}</td>
                    </tr>
                    <tr>
                        <td>Tasa Efectiva Anual</td>
                        <td>{tasa_efectiva_anual}</td>
                    </tr>
                    <tr>
                        <td>Ganancia estimada</td>
                        <td>{rendimientos_estimados}</td>
                    </tr>
                    <tr>
                        <td>Impuestos sobre las ganancias</td>
                        <td>{retefuente}</td>
                    </tr>
                    <tr>
                        <td>Ganancia total</td>
                        <td>{total_recibido}</td>
                    </tr>
                </tbody>
            </table>
            <hr> 
            """
    
    return f"""
    <!DOCTYPE html>
    <html lang="es">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Informe de Inversión</title>
        <style>
            /* Diseño general del cuerpo */
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f3f9f2; /* Suave verde pastel */
                display: flex;
                justify-content: center;
                align-items: flex-start;
                color: #333;
            }}

            h1 {{
                font-size: 2.5rem;
                color: #2c3e50;
                margin-bottom: 20px;
                font-weight: 600;
                text-align: center;
            }}

            h3 {{
                font-size: 1.8rem;
                color: #27ae60; /* Verde brillante */
                margin-bottom: 10px;
                font-weight: 600;
                border-bottom: 2px solid #27ae60; /* Línea debajo de los encabezados */
            }}

            p {{
                font-size: 1.1rem;
                color: #555;
                line-height: 1.8;
                margin-bottom: 20px;
            }}

            .highlight {{
                font-weight: 600;
                color: #2ecc71; /* Verde más brillante */
            }}

            /* Estilo de la tabla */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px 15px;
                text-align: left;
                font-size: 1rem;
            }}

            th {{
                background-color: #27ae60; /* Verde de fondo */
                color: white;
                text-align: center;
                font-weight: bold;
            }}

            td {{
                color: #555;
                font-weight: 500;
            }}

            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            tr:nth-child(odd) {{
                background-color: #ffffff;
            }}

            .encabezado {{
                font-family: 'Arial', sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: #333;
                text-align: center;
                margin: 20px 0;
                padding: 10px;
                background-color: #f4f4f4;
                border-radius: 8px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }}

            tr:hover {{
                background-color: #ecf9e3; /* Efecto hover en filas */
            }}

            hr {{
                border: 0;
                border-top: 2px solid #27ae60; /* Línea separadora verde */
                margin: 20px 0;
            }}

            .container {{
                width: 80%;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}

            h2 {{
                font-size: 2rem;
                color: #27ae60; /* Verde en el encabezado principal */
                text-align: center;
                margin-bottom: 30px;
            }}

        </style>
    </head>

    <body>
        <div class="container">

            <h2>Informe de la Inversión</h2>
            <h3 class="encabezado">Las tablas están ordenadas desde el banco que da mayor interes del CDT al menor</h3>

            <!-- Los bancos y sus tablas se generarán dinámicamente aquí -->
            {bancos_html}

            <p>Informe generado el <strong>{fecha_completa}</strong></p>

        </div>
    </body>

    </html>
    """

