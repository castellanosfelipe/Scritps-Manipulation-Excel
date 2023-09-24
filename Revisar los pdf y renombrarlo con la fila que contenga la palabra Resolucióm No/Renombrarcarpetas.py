# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 17:20:48 2023

@author: bpena
"""
import fitz
import os

def buscar_y_renombrar_pdf(ruta_carpeta):
    for root, subdirs, files in os.walk(ruta_carpeta):
        for archivo in files:
            if archivo.endswith(".pdf"):
                # Construir la ruta completa del archivo
                ruta_pdf = os.path.join(root, archivo)
                
                # Abrir el PDF
                pdf = fitz.open(ruta_pdf)
                
                # Inicializar una variable para almacenar el nuevo nombre
                nuevo_nombre = None
                
                # Leer solo la primera página
                primera_pagina = pdf.load_page(0)
                texto_pagina = primera_pagina.get_text()
                    
                # Dividir el texto en líneas
                lineas = texto_pagina.split('\n')
                    
                # Bandera para indicar si se encontró la frase
                resolucion_encontrada = False
                
                # Buscar la frase "Resolución No." en cada línea
                for linea in lineas:
                    if "Resolución No." in linea:
                        # Almacenar el nuevo nombre en lugar de renombrar de inmediato
                        nuevo_nombre = linea.strip() + "_" + archivo # Agregar el nombre original
                        resolucion_encontrada = True
                        break  # Salir del bucle de búsqueda en esta página
                
                # Si no se encontró la frase, renombrar el archivo agregando "_Revisar"
                if not resolucion_encontrada:
                    nuevo_nombre = "Revisar-" + archivo
                
                # Cerrar el PDF después de buscar en la primera página
                pdf.close()
                
                nuevo_path = os.path.join(root, nuevo_nombre)
                try:
                    os.rename(ruta_pdf, nuevo_path)
                    print(f"El archivo {archivo} ha sido renombrado como {nuevo_nombre}")
                except Exception as e:
                    print(f"Error al renombrar el archivo {archivo}: {e}")

# Uso del código
ruta_carpeta = "C:\\Users\\administrador\\Documents\\Renombrar\\con ocr\\INURBE RESOLUCIONES"  # Ruta de la carpeta que contiene los archivos PDF
buscar_y_renombrar_pdf(ruta_carpeta)



