import requests

def get_api_info(token,fechaInicio,fechaFin):   
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = 'http://localhost:5205/api/actividad-diaria/actividades-reporte-tr'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response
