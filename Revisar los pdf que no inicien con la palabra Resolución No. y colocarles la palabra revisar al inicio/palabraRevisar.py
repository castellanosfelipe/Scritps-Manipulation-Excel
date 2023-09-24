# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 15:36:57 2023

@author: bpena
"""
import os
import re

def renombrar_archivos(directorio):
    for root, dirs, files in os.walk(directorio):
        for nombre_archivo in files:
            if nombre_archivo.lower().endswith('.pdf'):
                ruta_completa = os.path.join(root, nombre_archivo)

                # Obtener el nombre del archivo sin extensión
                nombre_base, extension = os.path.splitext(nombre_archivo)

                # Verificar si el nombre cumple con el patrón
                if not re.match(r'^Resolución No\.\ \d{3}', nombre_base):
                    nuevo_nombre = f"revisar-{nombre_base}{extension}"
                    nueva_ruta = os.path.join(root, nuevo_nombre)
                    os.rename(ruta_completa, nueva_ruta)
                    print(f"Renombrado: {ruta_completa} -> {nueva_ruta}")

# Llama a la función y pasa el directorio que quieres analizar
directorio = "C:\\Users\\administrador\\Documents\\Renombrar\\con ocr\\INURBE RESOLUCIONES"  # Cambia esto con la ruta de tu directorio
renombrar_archivos(directorio)

