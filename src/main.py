import datetime
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.reports.excel.time_report.excel_timereport import get_report, get_report_client
import logging
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

@app.get('/', tags=['ReporteExcel'])
async def generar_timereport(token: str, fechaInicio: datetime.date, fechaFin: datetime.date, idUsuario: int | None = None):
    """
    Genera y devuelve un reporte de TimeReport en formato Excel.
    """
    try:
        return get_report(token,fechaInicio,fechaFin, idUsuario)     
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
    
@app.get('/cliente', tags=['ReporteExcelCliente'])
async def generar_timereport_cliente(token: str, fechaInicio: datetime.date, fechaFin: datetime.date, idCliente: int | None = None):
    """
    Genera y devuelve un reporte de TimeReport en formato Excel por Cliente.
    """
    try:
        return get_report_client(token,fechaInicio,fechaFin, idCliente)     
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
    