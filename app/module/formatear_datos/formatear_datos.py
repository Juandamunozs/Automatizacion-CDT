def monto_inicial (amount):
    amount = int(amount) 
    amount = "{:,}".format(amount)
    return amount

def monto_inicial_formateado(amount):
    amount = amount.replace(",", ".").replace("$ ", "")
    return f"$ {amount}"

def tasa_anual_formateado(amount):
    if isinstance(amount, str):
        amount = amount.replace(".", ",")
    return amount


def rendimiento_formateado(numero):
    if isinstance(numero, str):
        numero = numero.replace('$', '').replace(' ', '').strip()
        if ',' in numero:
            partes = numero.split(',')
            if len(partes[1]) == 3:  
                numero = partes[0] + '.' + partes[1]  
            else:
                numero = partes[0]  
    try:
        numero = int(numero)
    except ValueError:
        return "$ " + numero 
    numero = "{:,}".format(numero).replace(",", ".")
    return "$ " + numero

def limpiar_datos(banco):
    banco["montoInvertido"] = banco["montoInvertido"].replace("$", "").replace(",", "").strip()
    banco["rendimientosEstimados"] = banco["rendimientosEstimados"].replace("$", "").replace(",", "").strip()
    banco["retefuente"] = banco["retefuente"].replace("$", "").replace(",", "").strip()
    tasaEfectiva = banco["tasaEfectivaAnual"].replace("%", "").strip().replace(",", ".")
    banco["tasaEfectivaAnual"] = tasaEfectiva
    banco["totalRecibidoAlVencimiento"] = banco["totalRecibidoAlVencimiento"].replace("$", "").replace(",", "").strip()
    banco["totalRecibidoAlVencimiento"] = banco["totalRecibidoAlVencimiento"].replace(".", "")  
    if banco["totalRecibidoAlVencimiento"].endswith("00"):
        banco["totalRecibidoAlVencimiento"] = banco["totalRecibidoAlVencimiento"][:-2] 
    banco["totalRecibidoAlVencimiento"] = float(banco["totalRecibidoAlVencimiento"])  
    return banco["totalRecibidoAlVencimiento"]

def convertir_a_numero(amount):
    try:
        amount = amount.replace('$', '')
        if ',' in amount:
            amount = amount.split(',')[0]  
        amount = amount.replace(",", "")  
        amount = amount.replace(".", "")  
        return int(amount)
    except Exception as e:
        print(f"Error al convertir el valor: {e}")
        return 0  
    
def ordenar_bancos_por_tasa(res_investigacion):
    try:
        bancos_ordenados = sorted(
            res_investigacion.items(),
            key=lambda x: convertir_a_numero(x[1]['totalRecibidoAlVencimiento']),
            reverse=True  
        )
        return dict(bancos_ordenados)
    except Exception as e:
        print(f"Error al ordenar los bancos: {e}")
        return res_investigacion 
    
def convertir_a_numero_estimado(valor):
    try:
        valor = valor.replace('$', '').replace(',', '').strip()
        if ',' in valor:
            valor = valor.replace(",", ".")
        return float(valor)
    except Exception as e:
        print(f"Error al convertir el valor: {e}")
        return 0  