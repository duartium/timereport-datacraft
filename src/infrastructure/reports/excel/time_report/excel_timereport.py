import xlsxwriter
from datetime import datetime
import locale
import io
from fastapi.responses import StreamingResponse
from application.services.date_service import get_days_of_month, obtener_numero_mes_actual, obtener_dia_semana,es_fin_de_semana, handler_response
from application.services.excel_service import obtener_letra_columna
from infrastructure.external_services.ipmAPI_service import map_res, get_api_info
# res = {
#     "row1": {
#         "tipo" : "CAPACITACION",
#         "lider" : "SAC EDUARDO SANCHEZ",
#         "codigo" : "CONECEL",
#         "total" : 3.5
#     },
#     "row2": {
#         "tipo" : "REUNION",
#         "lider" : "SAC LENIN VELIZ",
#         "codigo" : "CONECEL",
#         "total" : 3.0
#     }
# }

def generar_timereport_excel():
    # Configura la localización para la fecha en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

    # Obtiene la fecha actual y el nombre del mes en español
    fecha_actual = datetime.now().strftime('%d%m%y')
    mes_actual = datetime.now().strftime('%B').capitalize()
    anio_actual = datetime.now().year
    numero_mes_Actual = obtener_numero_mes_actual()
    dias_del_mes = get_days_of_month(int(numero_mes_Actual))
    start_num_row = 8
    cols_fin_semana = []

    #Peticion GET al API
    res = get_api_info()
    # Crea un archivo de Excel en la memoria, no en el disco
    output = io.BytesIO()

    # Crea el nombre del archivo Excel basado en la fecha actual
    nombre_archivo_excel = f'TimeReport_{fecha_actual}.xlsx'

   
    # Crea un nuevo archivo Excel y añade una hoja de trabajo
    workbook = xlsxwriter.Workbook(output, {'in-memory': True})
    worksheet = workbook.add_worksheet()

    # Define los formatos que se utilizarán en la hoja
    bold_format = workbook.add_format({
        'bold': True, 
        'font_size': 12,
        'font_color': 'black'
    })
    title_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 22,
        'bold': True,
        'text_wrap': True
    })
    merge_format = workbook.add_format({
        'align': 'left',
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
    weekend_format = workbook.add_format({
        'border': 1,
        'bg_color': '#88C6F1'
    })
    # Combina celdas para los títulos de las columnas más amplias y escribe los títulos
    worksheet.merge_range('A3:B3', 'Cliente:', bold_format)
    worksheet.merge_range('A4:B4', 'Nombre del consultor:', bold_format)
    worksheet.merge_range('G2:H2', mes_actual.upper(), bold_format)
    worksheet.merge_range('J2:L2', str(anio_actual), bold_format)
    worksheet.merge_range('A5:A7', 'N°', header_format)
    worksheet.merge_range('B5:B7', 'TIPO DE ACTIVIDAD', header_format)
    worksheet.merge_range('C5:C7', 'LÍDER DE PROYECTO', header_format)
    worksheet.merge_range('D5:D7', 'CÓDIGO DE REQUERIMIENTO #\nCÓDIGO INCIDENCIA', header_format)
    worksheet.merge_range('E5:E7', 'DESCRIPCIÓN DE TRABAJOS REALIZADOS', header_format)
    worksheet.merge_range('F5:F7', 'TOTAL HORAS POR ACT.', header_format)
    col_distrib = obtener_letra_columna(len(dias_del_mes)+6)
    cell_range_distrib = f'G5:{col_distrib}5'
    worksheet.merge_range(cell_range_distrib, 'DISTRIBUCION DE TIEMPO POR DIA', header_format)
    col_horas = obtener_letra_columna(len(dias_del_mes)+7)
    cell_range_horas = f'{col_horas}5:{col_horas}7'
    worksheet.merge_range(cell_range_horas, 'TOTAL HORAS POR ACT.', header_format)
    
    titulo = f'A1:{col_horas}1'
    worksheet.merge_range(titulo, 'TIME REPORT', title_format)
     # Recorrer los días del mes y crear las columnas
    for i, day_num in enumerate(dias_del_mes, start=7):  # Comenzando en 1 para que la columna 'A' sea el índice 1
        column_letter = obtener_letra_columna(i)
        cell_range_num = f'{column_letter}6:{column_letter}6'
        cell_range_dia = f'{column_letter}7:{column_letter}7'
        dia = obtener_dia_semana(day_num)
        es_fin_de_semana(dia,column_letter,cols_fin_semana)
        worksheet.write_string(cell_range_num, day_num, header_format)
        worksheet.write_string(cell_range_dia, dia, header_format)

    # Configura el ancho de las columnas
    worksheet.set_column('A:A', 5)   # N°
    worksheet.set_column('B:B', 20)  # TIPO DE ACTIVIDAD
    worksheet.set_column('C:C', 25)  # LÍDER DE PROYECTO
    worksheet.set_column('D:D', 15)  # CÓDIGO DE REQUERIMIENTO 
    worksheet.set_column('E:E', 25)  # DESCRIPCION DE TRABAJOS REALIZADOS
    worksheet.set_column('F:F', 10)  # TOTAL HORAS
    letra_horas = f'{col_horas}:{col_horas}'
    worksheet.set_column(letra_horas, 10)  # TOTAL HORAS
    # ... Configura el ancho para las demás columnas ...

    # Escribir filas con datos
    n=1 #1 para que empiece en columna A
    for datos in res:
        num_row = start_num_row
        cell = f'A{num_row}'
        worksheet.write(cell, n, cell_format) #N°
        for col in cols_fin_semana: #Colorear dias de fin de semana
            cell_weekend = f'{col}{num_row}'
            worksheet.write(cell_weekend, '', weekend_format)      
        cell = f'B{num_row}'
        worksheet.write(cell, datos["tipoActividad"], cell_format)
        cell = f'C{num_row}'
        lideres =  "".join(datos["liderProyecto"])
        worksheet.write(cell, lideres, cell_format)
        cell = f'D{num_row}'
        worksheet.write(cell, datos["codigoProyecto"], cell_format)
        cell = f'E{num_row}'
        worksheet.write(cell, datos["descripcionActividad"], cell_format)
        
        n = n + 1
        start_num_row = start_num_row + 1
    
    #Totales
    cell = f'A{start_num_row}:D{start_num_row}'
    worksheet.merge_range(cell, 'Totales', header_format)
    # ... Añade los datos para las demás celdas ...

    # Cierra el archivo Excel
    workbook.close()
    output.seek(0)

     # Crea una respuesta de streaming para enviar el archivo Excel
    response = StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo_excel}"

    return response