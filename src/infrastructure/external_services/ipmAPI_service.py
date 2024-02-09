import requests

def get_api_info(token,fechaInicio,fechaFin,idUsuario=None):   
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = 'http://localhost:5205/api/actividad-diaria/actividades-reporte-tr'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin,
        "idUsuario" : idUsuario
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response

def get_info_clientes_usuarios(token, fechaInicio, fechaFin, idCliente):
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = 'http://localhost:5205/api/actividad-diaria/usuarios-cliente'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin,
        "idCliente" : idCliente
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response


def get_reporte_cliente(token, fechaInicio,fechaFin,idCliente):
    api_auth = "Bearer %s"%token 
    headers = {'Authorization': api_auth}
    api = 'http://localhost:5205/api/actividad-diaria/actividades-reporte-cliente'
    params = {
        "fechaInicio" : fechaInicio,
        "fechaFin" : fechaFin,
        "idCliente" : idCliente
    }
    res = requests.get(api, headers=headers, params=params) 
    response = res.json()
    return response
