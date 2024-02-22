import datetime
from fastapi import FastAPI, HTTPException, Header, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.reports.excel.time_report.handleResponses import get_report, get_report_client, get_report_usuario_cliente, get_report_all_users
from infrastructure.reports.excel.readExcel import leer_excel
import logging
from pydantic import BaseModel
import traceback    
app = FastAPI()
app.title = 'API generación de reportes de TimeReport IPM'
app.version = "0.0.1"

logger = logging.getLogger(__name__)

# Configura el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)
class BodyReportePost(BaseModel):
    fechaInicio: datetime.date
    fechaFin: datetime.date

class BodyUsuarioClientePost(BaseModel):
    fechaInicio: datetime.date
    fechaFin: datetime.date
    idUsuario: int 
    idCliente: int 

class BodyReporteClientePost(BaseModel):
    fechaInicio: datetime.date
    fechaFin: datetime.date
    idCliente: int 

@app.post('/api/generar-reporte-usuario', tags=['ReporteExcel'])
async def generar_timereport(body : BodyReportePost,token: str = Header(...)):
    """
    Método para generar reporte Excel para la pantalla de actividades desde la pantalla del consultor en Time Report. Genera un archivo excel en caso de que esté con un cliente y un archivo .zip en caso de que esté con más de uno.
    """
    try:
        return get_report(token,body.fechaInicio,body.fechaFin, None)     
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        stack_trace = traceback.format_exc()
        detail = {
            "error": str(e),
            "trace": stack_trace
        }
        logger.error(f"Error generando TimeReport: {str(e)}")
        raise HTTPException(status_code=500, detail=detail)
    
@app.post('/api/generar-reporte-usuario-cliente', tags=['ReporteExcelCliente'])
async def generar_timereport_usuario_por_cliente(body : BodyUsuarioClientePost,token: str = Header(...)):
    """
    Método para generar reporte Excel de un consultor en específico del cliente desde la pantalla administrativos en Time Report.
    """
    try:
        return get_report_usuario_cliente(token,body.fechaInicio,body.fechaFin, body.idUsuario, body.idCliente)     
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        stack_trace = traceback.format_exc()
        detail = {
            "error": str(e),
            "trace": stack_trace
        }
        logger.error(f"Error generando TimeReport: {str(e)}")
        raise HTTPException(status_code=500, detail=detail)
    
@app.post('/api/generar-reporte-cliente', tags=['ReporteExcelCliente'])
async def generar_timereport_cliente(body : BodyReporteClientePost,token: str = Header(...)):
    """
    Método para generar un archivo .zip con los reportes Excel de todos los consultores del cliente desde la pantalla de administrativos que deseen visualizar los reportes de actividades en Time Report.
    """
    try:
        if(body.idCliente == 0):
            return get_report_all_users(token,body.fechaInicio, body.fechaFin)
        else:
            return get_report_client(token,body.fechaInicio, body.fechaFin, body.idCliente)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        stack_trace = traceback.format_exc()
        detail = {
            "error": str(e),
            "trace": stack_trace
        }
        logger.error(f"Error generando TimeReport: {str(e)}")
        raise HTTPException(status_code=500, detail=detail)

@app.post('/api/leer-reporte', tags=['LeerReporteExcel'])
async def leer_reporte(file: UploadFile,token: str = Header(...)):
    try:
        contenido = await file.read()  # Espera la lectura del contenido del archivo
        return leer_excel(contenido, token)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        stack_trace = traceback.format_exc()
        detail = {
            "error": str(e),
            "trace": stack_trace
        }
        logger.error(f"Error importando TimeReport: {str(e)}")
        raise HTTPException(status_code=500, detail=detail)
