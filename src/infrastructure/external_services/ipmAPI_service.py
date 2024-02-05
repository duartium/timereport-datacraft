import requests
import base64
from application.services.date_service import obtener_inicio_fin_mes
def auth_login():
    email = 'cesar.centurion@integritysolutions.com.ec'
    password = '123'
    api_auth = 'http://localhost:5205/api/autenticacion/login'
    user = {
        'email' : email,
        'password' : password
    }
    res_auth = requests.post(api_auth, json=user)
    res_auth_json = res_auth.json()
    return res_auth_json['data']['token']

def get_api_info():   
    token = auth_login()
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = 'http://localhost:5205/api/actividad-diaria/obtener-por-fechas-tr'
    fechas = obtener_inicio_fin_mes()
    fecha_inicio = fechas[0]
    fecha_fin = fechas[1]
    params = {
        "fechaInicio" : fecha_inicio,
        "fechaFin" : fecha_fin,
        "UsuarioId" : 6021
    }
    res = requests.get(api, headers=headers, params=params) 
    posts = res.json()
    return posts

# def write_excel():
#     res = map_res()
#     n=1 #1 para que empiece en columna A
#     for(key,val) in res.items():
#         num_row = start_num_row
#         cell = f'A{num_row}'
#         worksheet.write(cell, n, cell_format) #N°
#         for col in cols_fin_semana: #Colorear dias de fin de semana
#             cell_weekend = f'{col}{num_row}'
#             worksheet.write(cell_weekend, '', weekend_format)
#         i=2 #2 para que empiece en columna B

#         for(key2,val2) in val.items():            
#             col = obtener_letra_columna(i)
#             cell = f'{col}{num_row}'            
#             worksheet.write(cell, val2,cell_format)
#             i = i + 1
#         n = n + 1
#         start_num_row = start_num_row + 1

def map_res():
    res = get_api_info()
    dic = {}    
    dic_principal = {}
    for actividad in res:
        dic["tipoActividad"] = actividad["tipoActividad"]
        dic["liderProyecto"] = actividad["liderProyecto"]
        dic["codigoProyecto"] = actividad["codigoProyecto"]
        dic["fechasHoras"] = actividad["fechasHoras"]
        dic_principal[actividad["descripcionActividad"]] = dic
    return dic_principal