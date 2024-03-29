from datetime import datetime, timedelta
def get_days_of_month(month, year=None):
    # Obtener el año actual si no se proporciona uno
    if year is None:
        year = datetime.now().year
    
    start_of_month = datetime(year, month, 1)
    if month == 12:
        # Si es diciembre, el próximo mes es enero del próximo año
        next_month = start_of_month.replace(year=year+1, month=1)
    else:
        # Para cualquier otro mes, solo incrementa el mes
        next_month = start_of_month.replace(month=month+1)
    
    # Calcula la diferencia de días entre el inicio del próximo mes y el inicio del mes actual
    days = [(start_of_month + timedelta(days=i)).day for i in range((next_month - start_of_month).days)]
    # Convierte los días en strings
    return [str(day) for day in days]

def obtener_numero_mes_actual():
    """
    Devuelve el número del mes actual.

    Returns:
        int: Número del mes actual (1 para Enero, 2 para Febrero, etc.).
    """
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Extraer el mes actual como un número y devolverlo
    numero_mes_actual = fecha_actual.month

    return numero_mes_actual

def obtener_nombre_mes(num):
    meses = {1:"Enero", 2: "Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
    return meses[num]

def obtener_dia_semana(fecha):
    dias = ['L','M','M','J','V','S','D']
    index = fecha.weekday()
    return dias[index]

def es_fin_de_semana(dia,col,arr):
    if(dia == 'S' or dia == 'D'):
        arr.append(col)
    return arr

def obtener_numero_mes(mes):
    meses = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12
    }
    return meses[mes]