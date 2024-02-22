from application.services.date_service import obtener_nombre_mes
from infrastructure.external_services.ipmAPI_service import get_api_info, get_reporte_cliente, get_api_info_usuario_cliente
import io
import zipfile
from infrastructure.reports.excel.time_report.excel_timereport import generar_timereport_excel
from fastapi.responses import StreamingResponse, Response, JSONResponse
import zipfile
import json
import base64
class ResponseBody:
    def __init__(self, tipo, archivo):
        self.type = tipo
        self.data = archivo
    def json(self):
        return {"type": self.type, "data": str(self.data)} 


def get_report(token,fechaInicio,fechaFin, idUsuario):
    res = get_api_info(token,fechaInicio,fechaFin, idUsuario) #peticion GET al API de IPM
    if res["data"] == None:
        return res["message"]
    else:
        res = res["data"]
        anio = fechaInicio.year
        mes = obtener_nombre_mes(fechaInicio.month)        
        clientes = set()
        files = []
        consultor = res[0]["nombreUsuario"].replace(" ", "_")
        nombre_archivo = f'TimeReport_{mes}_{anio}_{consultor}'
        for data in res:
            clientes.add(data["clienteProyecto"])
        if len(clientes) > 1 :   
            for cliente in clientes:
                res_filtrado = [item for item in res if item["clienteProyecto"] == cliente]            
                files.append(generar_timereport_excel(res_filtrado,fechaInicio))
            return zipfiles(files, nombre_archivo,clientes)
        else:
            file = generar_timereport_excel(res,fechaInicio)
            archivo_base64 = base64.b64encode(file.getvalue()).decode("utf-8")
            response = {"archivo": archivo_base64, "tipo": "EXCEL"}            
            return Response(content=json.dumps(response), media_type="application/json")

def get_report_usuario_cliente(token,fechaInicio,fechaFin, idUsuario, idCliente):
    res = get_api_info_usuario_cliente(token,fechaInicio,fechaFin, idUsuario,idCliente) #peticion GET al API de IPM
    if res["data"] == None:
        return res["message"]
    else:
        res = res["data"]
        anio = fechaInicio.year
        mes = obtener_nombre_mes(fechaInicio.month)        
        clientes = set()
        files = []
        consultor = res[0]["nombreUsuario"].replace(" ", "_")
        cliente = res[0]["clienteProyecto"].replace(" ", "_").replace("\r", "").replace("\n", "")
        nombre_archivo = f'TimeReport_{mes}_{anio}_{consultor}_{cliente}'
        for data in res:
            clientes.add(data["clienteProyecto"])
        if len(clientes) > 1 :   
            for cliente in clientes:
                res_filtrado = [item for item in res if item["clienteProyecto"] == cliente]            
                files.append(generar_timereport_excel(res_filtrado,fechaInicio))
            return zipfiles(files, nombre_archivo,clientes)
        else:
            file = generar_timereport_excel(res,fechaInicio)
            # response = StreamingResponse(file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            # response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo}.xlsx"
            # response.headers["Tipo"] = "EXCEL"
            # return response
            archivo_base64 = base64.b64encode(file.getvalue()).decode("utf-8")
            response = {"archivo": archivo_base64, "tipo": "EXCEL"}            
            return Response(content=json.dumps(response), media_type="application/json")

def get_report_all_users(token,fechaInicio,fechaFin):
    res = get_reporte_cliente(token,fechaInicio,fechaFin, 0)
    if res["data"] == None:
        return res["message"]
    else:
        res = res["data"]       
        anio = fechaInicio.year
        mes = obtener_nombre_mes(fechaInicio.month)        
        usuario_cliente = set()
        files = []
        nombre_archivo = f'TimeReport_{mes}_{anio}'
        for data in res:
            info_usuario_cliente = data["nombreUsuario"],data["nombreProyecto"], data["clienteProyecto"]
            usuario_cliente.add(info_usuario_cliente)
        if len(usuario_cliente) > 1 :   
            for usuario in usuario_cliente:
                res_filtrado = [item for item in res if (item["nombreUsuario"],item["nombreProyecto"], item["clienteProyecto"])  == usuario]         
                files.append(generar_timereport_excel(res_filtrado,fechaInicio))
            return zipfiles_all_usuarios(files, nombre_archivo,usuario_cliente)
        else:
            file = generar_timereport_excel(res,fechaInicio)
            # response = StreamingResponse(file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            # response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo}.xlsx"
            # response.headers["Tipo"] = "EXCEL"
            # return response
            archivo_base64 = base64.b64encode(file.getvalue()).decode("utf-8")
            response = {"archivo": archivo_base64, "tipo": "EXCEL"}            
            return Response(content=json.dumps(response), media_type="application/json")

def get_report_client(token,fechaInicio,fechaFin, idCliente):
    res = get_reporte_cliente(token,fechaInicio,fechaFin, idCliente) #peticion GET al API de IPM
    if res["data"] == None:
        return res["message"]
    else:
        res = res["data"]       
        anio = fechaInicio.year
        mes = obtener_nombre_mes(fechaInicio.month)        
        usuarios = set()
        files = []
        cliente = res[0]["clienteProyecto"].replace(" ", "_").replace("\r", "").replace("\n", "")
        nombre_archivo = f'TimeReport_{mes}_{anio}_{cliente}'
        for data in res:
            usuarios.add(data["nombreUsuario"])
        if len(usuarios) > 1 :   
            for usuario in usuarios:
                res_filtrado = [item for item in res if item["nombreUsuario"] == usuario]            
                files.append(generar_timereport_excel(res_filtrado,fechaInicio))
            return zipfiles_clientes(files, nombre_archivo,usuarios)
        else:
            file = generar_timereport_excel(res,fechaInicio)
            archivo_base64 = base64.b64encode(file.getvalue()).decode("utf-8")
            response = {"archivo": archivo_base64, "tipo": "EXCEL"}            
            return Response(content=json.dumps(response), media_type="application/json")

def zipfiles(file_objects, nombre_archivo,clientes):
    zip_filename = f"{nombre_archivo}.zip"
    clientes = list(clientes)
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED)

    for index, file_object in enumerate(file_objects):
        cliente = clientes[index]
        cliente = cliente.replace(" ", "_")
        fname =  f"{nombre_archivo}_{cliente}.xlsx" 

        zf.writestr(fname, file_object.getvalue())
    zf.close()

    # resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
    #     'Content-Disposition': f'attachment;filename={zip_filename}',
    #     'Tipo' : 'ZIP' 
    # })
    archivo_base64 = base64.b64encode(s.getvalue()).decode("utf-8")
    response = {"archivo": archivo_base64, "tipo": "ZIP"} 
    return Response(content=json.dumps(response), media_type="application/json")

def zipfiles_all_usuarios(file_objects, nombre_archivo,data):
    zip_filename = f"{nombre_archivo}.zip"
    data = list(data)
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED)

    for index, file_object in enumerate(file_objects):
        cliente = data[index][2]
        cliente = cliente.replace(" ", "_")
        usuario = data[index][0]
        usuario = usuario.replace(" ", "_")
        fname =  f"{nombre_archivo}_{usuario}_{cliente}.xlsx" 

        zf.writestr(fname, file_object.getvalue())
    zf.close()

    # resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
    #     'Content-Disposition': f'attachment;filename={zip_filename}',
    #     'Tipo' : 'ZIP' 
    # })
    archivo_base64 = base64.b64encode(s.getvalue()).decode("utf-8")
    response = {"archivo": archivo_base64, "tipo": "ZIP"} 
    return Response(content=json.dumps(response), media_type="application/json")

def zipfiles_clientes(file_objects, nombre_archivo,usuarios):
    zip_filename = f"{nombre_archivo}.zip"
    usuarios = list(usuarios)
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED)

    for index, file_object in enumerate(file_objects):
        usuario = usuarios[index]
        usuario = usuario.replace(" ", "_")
        fname =  f"{nombre_archivo}_{usuario}.xlsx" 

        zf.writestr(fname, file_object.getvalue())

    zf.close()
    archivo_base64 = base64.b64encode(s.getvalue()).decode("utf-8")
    response = {"archivo": archivo_base64, "tipo": "ZIP"}            
    # resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
    #     'Content-Disposition': f'attachment;filename={zip_filename}',
    #     'Tipo' : 'ZIP' 
    # })

    return Response(content=json.dumps(response), media_type="application/json")