from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reports.excel.time_report.excel_timereport import generar_timereport_excel

app = FastAPI()
app.title = 'API generación de reportes de TimeReport IPM'
app.version = "0.0.1"

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
    return generar_timereport_excel()
    
