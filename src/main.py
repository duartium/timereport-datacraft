from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.reports.excel.time_report.excel_timereport import generar_timereport_excel
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