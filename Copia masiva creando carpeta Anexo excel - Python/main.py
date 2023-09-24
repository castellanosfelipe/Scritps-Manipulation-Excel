
import filecmp
import os
import shutil

# Rutas de los dos directorios 
directorio1 = 'C:\scj\CDS_2017_FINAL\SCJ'
directorio2 = 'C:\scj\H2017\SCJ'

# Comparación entre los dos directorios
comparador = filecmp.dircmp(directorio1, directorio2)

# Función para crear la carpeta "anexos" en una ubicación dada
def crear_carpeta_anexos(directorio):
    anexos_path = os.path.join(directorio, 'Anexos')
    os.makedirs(anexos_path, exist_ok=True)

# Función para copiar todos los archivos y subcarpetas de una ubicación a otra
def copiar_archivos_y_subcarpetas(origen, destino):
    for root, dirs, files in os.walk(origen):
        destino_root = os.path.join(destino, os.path.relpath(root, origen))
        
        # Crea la carpeta en el destino si no existe
        os.makedirs(destino_root, exist_ok=True)
        
        # Copia los archivos en el destino
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
            
# luego copia todos los archivos y subcarpetas al directorio de destino
for carpeta_igual in comparador.common_dirs:
    carpeta2_path = os.path.join(directorio2, carpeta_igual)
    
    # Crea la carpeta "anexos" en la ubicación del directorio de destino
    crear_carpeta_anexos(carpeta2_path)
    
    # Copia todos los archivos y subcarpetas de la carpeta igual a la carpeta "anexos"
    carpeta1_path = os.path.join(directorio1, carpeta_igual)
    copiar_archivos_y_subcarpetas(carpeta1_path, os.path.join(carpeta2_path, 'Anexos'))


print("Proceso completado. Las carpetas iguales en el directorio de destino ahora tienen una carpeta 'anexos' y se han copiado todos los archivos y subcarpetas.")

