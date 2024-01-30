import xlsxwriter
from datetime import datetime
import locale
import io
from fastapi.responses import StreamingResponse
from application.services.date_service import get_days_of_month, obtener_numero_mes_actual
from application.services.excel_service import obtener_letra_columna

def generar_timereport_excel():
    # Configura la localización para la fecha en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

    # Obtiene la fecha actual y el nombre del mes en español
    fecha_actual = datetime.now().strftime('%d%m%y')
    mes_actual = datetime.now().strftime('%B').capitalize()
    numero_mes_ACtual = obtener_numero_mes_actual()

    # Crea un archivo de Excel en la memoria, no en el disco
    output = io.BytesIO()

    # Crea el nombre del archivo Excel basado en la fecha actual
    nombre_archivo_excel = f'TimeReport_{fecha_actual}.xlsx'

   
    # Crea un nuevo archivo Excel y añade una hoja de trabajo
    workbook = xlsxwriter.Workbook(output, {'in-memory': True})
    worksheet = workbook.add_worksheet()

    # Define los formatos que se utilizarán en la hoja
    bold_format = workbook.add_format({'bold': True, 'font_color': 'black'})
    merge_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'bg_color': '#C0C0C0'  # Amarillo
    })
    header_format = workbook.add_format({
        'bg_color': '#C0C0C0',  # Gris
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'text_wrap': True
    })
    cell_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })

    # Combina celdas para los títulos de las columnas más amplias y escribe los títulos
    worksheet.merge_range('A1:A3', 'N°', merge_format)
    worksheet.merge_range('B1:B3', 'TIPO DE ACTIVIDAD', merge_format)
    worksheet.merge_range('C1:C3', 'LÍDER DE PROYECTO', merge_format)
    worksheet.merge_range('D1:D3', 'CÓDIGO DE REQUERIMIENTO #\nCÓDIGO INCIDENCIA', header_format)
    worksheet.merge_range('E1:E3', 'DESCRIPCIÓN DE TRABAJOS REALIZADOS', header_format)
    worksheet.merge_range('F1:F3', 'TOTAL HORAS POR ACT.', merge_format)

    print(type(mes_actual))
    dias_del_mes = get_days_of_month(int(mes_actual))

    worksheet.merge_range('G1:AJ1', 'DISTRIBUCION DE TIEMPO POR DIA', merge_format)
    

     # Recorrer los días del mes y crear las columnas
    for i, day in enumerate(dias_del_mes, start=1):  # Comenzando en 1 para que la columna 'A' sea el índice 1
        column_letter = obtener_letra_columna(i)
        cell_range = f'{column_letter}2:{column_letter}2'
        worksheet.merge_range(cell_range, day, header_format)

    # Configura el ancho de las columnas
    worksheet.set_column('A:A', 5)   # N°
    worksheet.set_column('B:B', 20)  # TIPO DE ACTIVIDAD
    worksheet.set_column('C:C', 25)  # LÍDER DE PROYECTO
    # ... Configura el ancho para las demás columnas ...

    # Añade algunas filas de ejemplo con datos
    worksheet.write('A4', 1, cell_format)
    worksheet.write('B4', 'Análisis', cell_format)
    worksheet.write('C4', 'prueba', cell_format)
    # ... Añade los datos para las demás celdas ...

    # Cierra el archivo Excel
    workbook.close()
    output.seek(0)

     # Crea una respuesta de streaming para enviar el archivo Excel
    response = StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo_excel}"

    return response