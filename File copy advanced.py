# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:22:19 2024

@author: bpena
"""

import filecmp
import os
import shutil

# Rutas de los dos directorios 
directorio1 = 'C:\test\anexos'
directorio2 = 'C:\test\contratos'

comparador = filecmp.dircmp(directorio1, directorio2)

def crear_carpeta_anexos(directorio):
    anexos_path = os.path.join(directorio, 'Anexos')
    os.makedirs(anexos_path, exist_ok=True)

def copiar_archivos_y_subcarpetas(origen, destino):
    for root, dirs, files in os.walk(origen):
        destino_root = os.path.join(destino, os.path.relpath(root, origen))
        
        os.makedirs(destino_root, exist_ok=True)
        
        for file in files:
            origen_file = os.path.join(root, file)
            destino_file = os.path.join(destino_root, file)
            shutil.copy2(origen_file, destino_file)
            
def copiar_todo_el_directorio(origen, destino):
    for item in os.listdir(origen):
        origen_item = os.path.join(origen, item)
        destino_item = os.path.join(destino, item)
        
        if os.path.isdir(origen_item):
            copiar_todo_el_directorio(origen_item, destino_item)
        else:
            shutil.copy2(origen_item, destino_item)
            
for carpeta_igual in comparador.common_dirs:
    carpeta2_path = os.path.join(directorio2, carpeta_igual)
    
    crear_carpeta_anexos(carpeta2_path)
    
    carpeta1_path = os.path.join(directorio1, carpeta_igual)
    copiar_archivos_y_subcarpetas(carpeta1_path, os.path.join(carpeta2_path, 'Anexos'))

print("Proceso completado. Las carpetas iguales en el directorio de destino ahora tienen una carpeta 'anexos' y se han copiado todos los archivos y subcarpetas.")