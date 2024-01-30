def obtener_letra_columna(column_index):
    letter = ''
    while column_index > 0:
        column_index, remainder = divmod(column_index - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter

