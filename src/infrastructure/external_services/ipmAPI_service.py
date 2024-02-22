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

def post_importar_excel(actividades, token):
    api_auth = "Bearer %s"%token 
    headers = {'accept': '*/*',
               'Authorization': api_auth}
    api = url + 'importar-excel'
    try:
        res = requests.post(api, json=actividades, headers=headers)
        res.raise_for_status()  # Genera una excepción para errores HTTP
        if res.text:
            response = res.json()
            return response
        else:
            print("La respuesta está vacía.")
            return None
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except ValueError as e:
        raise Exception(e)
