import xlsxwriter
from datetime import datetime
import locale

def generar_timereport_excel():
    fecha_actual = datetime.now().strftime('%d%m%y')
    nombre_archivo_excel = f'TimeReport_{fecha_actual}.xlsx'

    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8' or 'Spanish_Spain.1252')
    mes_actual = datetime.now().strftime('%B')

    workbook = xlsxwriter.Workbook(nombre_archivo_excel)
    worksheet = workbook.add_worksheet(f"TimeReport_{mes_actual}")

    worksheet.write(0, 0, "#")
    worksheet.write(0, 1, "Name")
    worksheet.write(0, 2, "Phone")
    worksheet.write(0, 3, "Email")

    workbook.close()
    return "OK"