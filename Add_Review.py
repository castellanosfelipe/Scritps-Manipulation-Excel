# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:17:31 2024

@author: bpena
"""

import os
import re

def renombrar_archivos(directorio):
    for root, dirs, files in os.walk(directorio):
        for nombre_archivo in files:
            if nombre_archivo.lower().endswith('.pdf'):
                ruta_completa = os.path.join(root, nombre_archivo)

                nombre_base, extension = os.path.splitext(nombre_archivo)

                if not re.match(r'^Resolución No\.\ \d{3}', nombre_base):
                    nuevo_nombre = f"revisar-{nombre_base}{extension}"
                    nueva_ruta = os.path.join(root, nuevo_nombre)
                    os.rename(ruta_completa, nueva_ruta)
                    print(f"Renombrado: {ruta_completa} -> {nueva_ruta}")

directorio = "C:\\Users\\test" 
renombrar_archivos(directorio)