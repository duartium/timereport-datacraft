import requests

url = 'http://localhost:5205/api/actividad-diaria/'

def get_api_info(token,fechaInicio,fechaFin,idUsuario=None):   
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = url + 'actividades-reporte-tr'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin,
        "idUsuario" : idUsuario
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response

def get_api_info_usuario_cliente(token,fechaInicio,fechaFin,idUsuario, idCliente):   
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = url + 'actividades-reporte-usuario-cliente'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin,
        "idCliente" : idCliente,
        "idUsuario" : idUsuario
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response


def get_reporte_cliente(token, fechaInicio,fechaFin,idCliente):
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = url + 'actividades-reporte-cliente'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin,
        "idCliente" : idCliente
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response
