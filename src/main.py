from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.reports.excel.time_report.excel_timereport import generar_timereport_excel
from infrastructure.external_services.ipmAPI_service import get_api_info
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


def generar_timereport():
    """
    Genera y devuelve un reporte de TimeReport en formato Excel.
    """
    try:
        return generar_timereport_excel()
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
    
@app.get('/api', tags =['Prueba API'])
def obtener_api():
    """
    Petición GET a API de IPM
    """
    try:
        return get_api_info()
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