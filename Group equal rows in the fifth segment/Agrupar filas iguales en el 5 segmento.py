# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 08:19:21 2023

@author: bpena
"""
import openpyxl

# Abre el archivo de Excel
nombre_archivo = 'Metadato.xlsx'
wb = openpyxl.load_workbook(nombre_archivo)
hoja = wb.active

# Diccionario para almacenar las filas agrupadas por el quinto segmento
grupos = {}

# Recorre todas las filas en la columna A
for fila in hoja.iter_rows(min_row=2, max_col=1, values_only=True):
    valor = fila[0]
    
    # Verifica si la celda está vacía
    if valor is not None:
        # Divide el valor por '\' y obtén el quinto segmento
        segmentos = valor.split('\\')
        if len(segmentos) >= 5:
            quinto_segmento = segmentos[4]
            
            # Agrega la fila al grupo correspondiente en el diccionario
            if quinto_segmento in grupos:
                grupos[quinto_segmento].append(valor)
            else:
                grupos[quinto_segmento] = [valor]

# Escribe los grupos en celdas separadas en la columna B
fila_resultado = 2
for quinto_segmento, filas in grupos.items():
    celda_resultado = 'B' + str(fila_resultado)
    hoja[celda_resultado] = '||'.join(filas)
    fila_resultado += 1

# Guarda los cambios en el archivo
wb.save('resultado.xlsx')

# Cierra el archivo de Excel
wb.close()
