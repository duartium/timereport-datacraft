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
    api = 'http://localhost:5205/api/actividad-diaria/actividades-reporte-tr'
    fechas = obtener_inicio_fin_mes()
    fecha_inicio = fechas[0]
    fecha_fin = fechas[1]
    params = {
        "fechaInicio" : fecha_inicio,
        "fechaFin" : fecha_fin,
        "UsuarioId" : 6021
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response
