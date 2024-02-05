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

def obtener_dia_semana(dia):
    dias = ['L','M','M','J','V','S','D']
    fecha_actual = datetime.now()
    mes = str(fecha_actual.month)
    year = str(fecha_actual.year)
    fecha = dia + '/' + mes + '/' + year
    fecha = datetime.strptime(fecha, "%d/%m/%Y")
    index = fecha.weekday()
    return dias[index]

def es_fin_de_semana(dia,col,arr):
    if(dia == 'S' or dia == 'D'):
        arr.append(col)
    return arr

res = {
  "success": "true",
  "message": "OK",
  "data": [
            {
            "proyecto":  
                {
                    "codigoProyecto" : "BB_FS_MEJ_FIRMAS_2023",
                    "liderProyecto" : "BYRON ANDRES DUARTE MOREJON",
                    "nombreProyecto": "Mejoras en proceso de escaneo de firmas COBIS",
                    "actividades":
                    [
                        {
                            "descripcionActividad": "Diseño",
                            "tipoActividad": "Diseño",
                            "fechas":
                                [
                                    {
                                        "fechaActividad": "2024-02-01T00:00:00",
                                        "cantidadHoras": 5
                                    },
                                    {
                                        "fechaActividad":  "2024-02-02T00:00:00",
                                        "cantidadHoras":  3
                                    }
                                ]				
                        },
                        {
                            "descripcionActividad":  "Funcionalidades",
                            "tipoActividad":  "Reunión",
                            "fechas": 
                                [
                                    {
                                        "fechaActividad":  "2024-02-05T00:00:00",
                                        "cantidadHoras":  8
                                    },
                                    {
                                        "fechaActividad":  "2024-02-06T00:00:00",
                                        "cantidadHoras":  5
                                    }
                                ]				
                        }
                    ]
                }
        }
    ]
}

def handler_response():
    proyectos = res["data"]
    for proyecto in proyectos:
        cod_proyecto = proyecto["proyecto"]["codigoProyecto"]
        lider_proyecto = proyecto["proyecto"]["liderProyecto"]
        actividades = proyecto["proyecto"]["actividades"]
        for actividad in actividades:
            tipo = actividad["tipoActividad"]
            fechas = actividad["fechas"]
            duracion_total = 0
            print("Tipo de actividad %s" %tipo)
            for fecha in fechas:
                fechaActividad = fecha["fechaActividad"]
                cantidadHoras = fecha["cantidadHoras"]
                duracion_total = duracion_total + cantidadHoras
                print(fechaActividad, cantidadHoras)
                
            print("Total de horas: %d" %duracion_total)
        print ("Codigo proyecto: %s"%cod_proyecto)
        print ("Lider proyecto: %s"%lider_proyecto)

    

def obtener_inicio_fin_mes():
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    dias = len(get_days_of_month(mes_actual))
    inicio = f"{mes_actual}/01/{año_actual}"
    fin = f"{mes_actual}/{dias}/{año_actual}"
    fecha_inicio = datetime.strptime(inicio, '%m/%d/%Y')
    fecha_fin = datetime.strptime(fin, '%m/%d/%Y')
    return [inicio, fin]