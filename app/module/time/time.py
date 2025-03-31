import datetime
import holidays

# Función para obtener el mes actual en texto (en español)
def obtener_mes_texto():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = meses[datetime.datetime.now().month - 1]
    return mes_actual

# Función para obtener el mes actual en número
def obtener_mes_numero():
    return datetime.datetime.now().month

# Función obtener hora completa
def obtener_hora_completa():
    ahora = datetime.datetime.now()
    hora = ahora.hour
    minuto = ahora.minute
    segundo = ahora.second
    return f"{hora:02}:{minuto:02}:{segundo:02}"

# Función para obtener el año actual
def obtener_anio():
    return datetime.datetime.now().year

# Función para obtener el día en número (siempre el día actual)
def obtener_dia_numero():
    return datetime.datetime.now().day

# Función para obtener el día de la semana en texto (en español)
def obtener_dia_texto(dia_del_mes=None):
    if dia_del_mes is None:
        dia_del_mes = obtener_dia_numero()  
    
    try:
        fecha_actual = datetime.datetime.now().date()
        fecha_dia = datetime.date(fecha_actual.year, fecha_actual.month, dia_del_mes)  
        dia_semana_ingles = fecha_dia.strftime("%A") 
        
        dias_semana_esp = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        dia_semana_espanol = dias_semana_esp.get(dia_semana_ingles, "Día no válido")
        return dia_semana_espanol
    
    except ValueError:
        return "Día no válido"  

def dias_festivos_colombia(dia=None, mes=None):
    if mes is None:
        mes = obtener_mes_numero()  
    if dia is None:
        dia = obtener_dia_numero()  
    
    dias_festivos_colombia = holidays.Colombia()  
    try:
        fecha_completa = datetime.date(obtener_anio(), mes, dia)

        if fecha_completa in dias_festivos_colombia:
            return f"Dia festivo debido a {dias_festivos_colombia[fecha_completa]}"
        else:
            return f""
    except ValueError:
        return "Fecha no válida."  
    
def calcular_fecha_futura(dias):
    fecha_futura = datetime.datetime.now() + datetime.timedelta(days=dias)
    
    return fecha_futura.strftime("%d/%m/%Y")

def formatear_segundos(tiempo):
    tiempo = float(tiempo)
    horas = int(tiempo // 3600)  
    minutos = int((tiempo % 3600) // 60) 
    segundos = int(tiempo % 60)  
    return f"{horas} horas {minutos} minutos {segundos} segundos"

