# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:09:24 2024

@author: bpena
"""

import fitz
import os

def buscar_y_renombrar_pdf(ruta_carpeta):
    for root, subdirs, files in os.walk(ruta_carpeta):
        for archivo in files:
            if archivo.endswith(".pdf"):
                ruta_pdf = os.path.join(root, archivo)    
                pdf = fitz.open(ruta_pdf)
                
                nuevo_nombre = None
                
                primera_pagina = pdf.load_page(0)
                texto_pagina = primera_pagina.get_text()
                lineas = texto_pagina.split('\n')
                resolucion_encontrada = False
                
                for linea in lineas:
                    if "Resolución No." in linea:
                        nuevo_nombre = linea.strip() + "_" + archivo 
                        resolucion_encontrada = True
                        break  
                
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
ruta_carpeta = "C:\\Users\\test" 
buscar_y_renombrar_pdf(ruta_carpeta)
