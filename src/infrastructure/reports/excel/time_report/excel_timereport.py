import xlsxwriter
import datetime
import locale
import io
import zipfile
from fastapi.responses import StreamingResponse, Response
from application.services.date_service import get_days_of_month, obtener_dia_semana,es_fin_de_semana, obtener_nombre_mes
from application.services.excel_service import obtener_letra_columna
from infrastructure.external_services.ipmAPI_service import get_api_info


def get_report(token,fechaInicio,fechaFin):
    res = get_api_info(token,fechaInicio,fechaFin) #peticion GET al API de IPM
    if len(res) == 0:
        return None
    else:
        anio = fechaInicio.year
        mes = obtener_nombre_mes(fechaInicio.month)        
        clientes = []
        files = []
        consultor = res[0]["nombreUsuario"].replace(" ", "_")
        nombre_archivo = f'TimeReport_{mes}_{anio}_{consultor}'
        for data in res:
            if data["clienteProyecto"] not in clientes:
                clientes.append(data["clienteProyecto"])
        if len(clientes) > 1 :   
            for cliente in clientes:
                res_filtrado = [item for item in res if item["clienteProyecto"] == cliente]            
                files.append(generar_timereport_excel(res_filtrado,fechaInicio))
            return zipfiles(files, nombre_archivo,clientes)
        else:
            file = generar_timereport_excel(res,fechaInicio)
            response = StreamingResponse(file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo}.xlsx"
            return response

def zipfiles(file_objects, nombre_archivo,clientes):
    zip_filename = f"{nombre_archivo}.zip"

    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED)

    for index, file_object in enumerate(file_objects):
        cliente = clientes[index]
        cliente = cliente.replace(" ", "_")
        # Calculate path for file in zip
        fname =  f"{nombre_archivo}_{cliente}.xlsx" 

        # Add file, at correct path
        zf.writestr(fname, file_object.getvalue())

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return resp

def generar_timereport_excel(res, fechaInicio):
    # Configura la localización para la fecha en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

    # Obtiene los dias del mes
    dias_del_mes = get_days_of_month(fechaInicio.month)
    mes = obtener_nombre_mes(fechaInicio.month)
    count_row = 8 #para que empiece desde la fila 8
    cols_fin_semana = []

    #Cliente
    cliente = res[0]["clienteProyecto"]
    #Consultor
    consultor = res[0]["nombreUsuario"]
    
    # Crea un archivo de Excel en la memoria, no en el disco
    output = io.BytesIO()

   
    # Crea un nuevo archivo Excel y añade una hoja de trabajo
    workbook = xlsxwriter.Workbook(output, {'in-memory': True})
    worksheet = workbook.add_worksheet()

    # Define los formatos que se utilizarán en la hoja
    bold_format = workbook.add_format({
        'bold': True, 
        'font_size': 12,
        'font_color': 'black'
    })
    bold_format_center = workbook.add_format({
        'bold': True, 
        'font_size': 12,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'black'
    })
    bottom_border = workbook.add_format({
        'bottom': 1
    })
    title_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 22,
        'bold': True,
        'text_wrap': True
    })
    header_format = workbook.add_format({
        'bg_color': '#C0C0C0',  # Gris
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 9,
        'bold': True,
        'text_wrap': True
    })
    cell_format = workbook.add_format({
        'border': 1,
        'font_size': 9,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })
    weekend_format = workbook.add_format({
        'border': 1,
        'bg_color': '#88C6F1'
    })
    format_decimal = workbook.add_format({
        'num_format': '#,##0.00',
        'border': 1,
        'font_size': 9,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
        })
    format_total = workbook.add_format({
        'num_format': '#,##0.00',
        'border': 1,
        'font_size': 11,
        'align': 'center',
        'color' : 'blue',
        'bold': True, 
        'valign': 'vcenter',
        'text_wrap': True
        })
    format_blue_font = workbook.add_format({
        'num_format': '#,##0.00',
        'border': 1,
        'font_size': 9,
        'align': 'center',
        'color' : 'blue',
        'valign': 'vcenter',
        'bold': True, 
        'text_wrap': True
    })
    format_green_font = workbook.add_format({
        'num_format': '#,##0.00',
        'border': 1,
        'font_size': 9,
        'align': 'center',
        'color' : 'green',
        'valign': 'vcenter',
        'bold': True, 
        'text_wrap': True
    })
    format_with_border = workbook.add_format({
    'border': 1
    })
    format_vacaciones = workbook.add_format({
        'border': 1,
        'bg_color': '#fcc614',
        'font_size': 11,
        'text_wrap': True
    })
    format_feriado = workbook.add_format({
        'border': 1,
        'bg_color': 'yellow',
        'font_size': 11,
        'text_wrap': True
    })
    format_permiso = workbook.add_format({
        'border': 1,
        'bg_color': '#2b9425',
        'font_size': 11,
        'text_wrap': True
    })
    # Combina celdas para los títulos de las columnas más amplias y escribe los títulos
    worksheet.merge_range('A3:B3', "Cliente: ", bold_format)
    worksheet.merge_range('C3:D3', cliente, bold_format)
    worksheet.merge_range('A4:B4', "Nombre del consultor:", bold_format)
    worksheet.merge_range('C4:D4', consultor, bold_format)
    worksheet.merge_range('G2:H2', mes.upper(), bold_format)
    worksheet.merge_range('J2:L2', fechaInicio.year, bold_format)
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
    for i, day_num in enumerate(dias_del_mes, start=7): 
        column_letter = obtener_letra_columna(i)
        cell_range_num = f'{column_letter}6:{column_letter}6'
        cell_range_dia = f'{column_letter}7:{column_letter}7'
        fecha = datetime.date(fechaInicio.year, fechaInicio.month, int(day_num))
        dia = obtener_dia_semana(fecha)
        es_fin_de_semana(dia,column_letter,cols_fin_semana)
        worksheet.write_string(cell_range_num, day_num, header_format)
        worksheet.write_string(cell_range_dia, dia, header_format)
        worksheet.set_column(f'{column_letter}:{column_letter}', 5)

    # Configura el ancho de las columnas
    worksheet.set_column('A:A', 5)   # N°
    worksheet.set_column('B:B', 20)  # TIPO DE ACTIVIDAD
    worksheet.set_column('C:C', 25)  # LÍDER DE PROYECTO
    worksheet.set_column('D:D', 30)  # CÓDIGO DE REQUERIMIENTO 
    worksheet.set_column('E:E', 60)  # DESCRIPCION DE TRABAJOS REALIZADOS
    worksheet.set_column('F:F', 15)  # TOTAL HORAS
    letra_horas = f'{col_horas}:{col_horas}'
    worksheet.set_column(letra_horas, 15)  # TOTAL HORAS, ultima columna
    # ... Configura el ancho para las demás columnas ...

    # Escribir filas con datos
    n=1 #1 para que empiece en columna A
    for datos in res:
        num_row = count_row
        cell = f'A{num_row}'
        worksheet.write(cell, n, header_format) #N°
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
        i=6 # columna F
        total_horas = 0
        for fecha in datos["fechasHoras"]:                        
            dia = int(fecha["fecha"].split("-")[2].split("T")[0])            
            col_cell = obtener_letra_columna(i+dia)            
            cell = f'{col_cell}{num_row}'
            worksheet.write_number(cell, float(fecha["horas"]), format_decimal)
            total_horas += float(fecha["horas"])
        cell = f'F{num_row}'
        col_cell = obtener_letra_columna(len(dias_del_mes)+6)
        cell_horas = f'G{num_row}:{col_cell}{num_row}'
        formula = f'=SUM({cell_horas})'
        worksheet.write_formula(cell, formula,format_decimal)
        # worksheet.write(cell, float(total_horas), format_decimal)
        cell = f'{col_horas}{num_row}'
        worksheet.write(cell, float(total_horas), format_decimal)
        n = n + 1
        count_row = count_row + 1
    
    #Totales
    cell = f'A{count_row}:E{count_row}'
    worksheet.merge_range(cell, 'Totales', header_format)
    cell_total = f'F{count_row}'    
    formula = f'=SUM(F8:F{count_row-1})'
    worksheet.write_formula(cell_total, formula,format_total)
    cell_total = f'{col_horas}{count_row}'  
    formula = f'=SUM({col_horas}8:{col_horas}{count_row-1})'
    worksheet.write_formula(cell_total, formula,format_total)
    #Subtotal por dia
    formula = f'=SUM(F8:F{count_row-1})'
    worksheet.write_formula(cell_total, formula,format_total)
    for i, day_num in enumerate(dias_del_mes, start=7):  
        column_letter = obtener_letra_columna(i)
        cell_subtotal = f'{column_letter}{count_row}'
        formula = f'=SUM({column_letter}8:{column_letter}{count_row-1})'
        worksheet.write_formula(cell_subtotal, formula,format_decimal)
        worksheet.conditional_format(cell_subtotal, {'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': 0,
                                             'format': format_blue_font})
        worksheet.conditional_format(cell_subtotal, {'type': 'cell',
                                             'criteria': 'not equal to',
                                             'value': 0,
                                             'format': format_green_font})

    #Firmas
    cell_firma = f'B{count_row+3}:C{count_row+3}'
    worksheet.merge_range(cell_firma,"", bottom_border)
    cell_elaborado = f'B{count_row+4}:C{count_row+4}'
    worksheet.merge_range(cell_elaborado, f'Elaborado por: {consultor}', bold_format_center)
    cell_firma = f'J{count_row+3}:V{count_row+3}'
    worksheet.merge_range(cell_firma,"", bottom_border)
    cell_elaborado = f'J{count_row+4}:V{count_row+4}'
    worksheet.merge_range(cell_elaborado, f'Revisado y Aprobado por: {cliente}', bold_format_center)

    #Nomenclaturas
    cell_nomenclatura = f'B{count_row+7}:B{count_row+10}'
    worksheet.merge_range(cell_nomenclatura,"Nomenclatura", cell_format)
    worksheet.write(f'C{count_row+7}', "Vacaciones",format_vacaciones)
    worksheet.write(f'C{count_row+8}', "Feriado",format_feriado)
    worksheet.write(f'C{count_row+9}', "Permiso",format_permiso)
    worksheet.write(f'C{count_row+10}', "Fines de semana",weekend_format)

    #Bordes para toda la celda
    cell_border = f'G8:{col_horas}{count_row}'
    worksheet.conditional_format(cell_border , { 'type' : 'blanks' , 'format' : format_with_border} )
    # Cierra el archivo Excel
    workbook.close()
    output.seek(0)

     # Crea una respuesta de streaming para enviar el archivo Excel
    # response = StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo}"

    return output