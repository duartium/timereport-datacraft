import datetime
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.reports.excel.time_report.excel_timereport import get_report, get_report_client
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

class BodyReporteUserPost(BaseModel):
    fechaInicio: datetime.date
    fechaFin: datetime.date
    idUsuario: int | None = None
class BodyReporteClientePost(BaseModel):
    fechaInicio: datetime.date
    fechaFin: datetime.date
    idCliente: int 

@app.post('/api/generar-reporte-usuario', tags=['ReporteExcel'])
async def generar_timereport(body : BodyReportePost,token: str = Header(...)):
    """
    Método para generar reporte Excel para la pantalla de actividades desde usuario en Time Report.
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
    
@app.post('/api/generar-reporte', tags=['ReporteExcel'])
async def generar_timereport(body : BodyReporteUserPost,token: str = Header(...)):
    """
    Método para generar reporte Excel por consultor desde la pantalla de reportes de administrativos en Time Report.
    """
    try:
        return get_report(token,body.fechaInicio,body.fechaFin, body.idUsuario)     
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
    Método para generar reporte Excel para la pantalla de administrativos que deseen visualizar los reportes de actividades en Time Report.
    """
    try:
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
    