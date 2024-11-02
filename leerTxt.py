import os

def leer_archivo(carpeta, nombre_archivo):
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'r') as archivo:
        return archivo.read().strip()
def escribir_archivo (carpeta, nombre_archivo,nuevo_contenido):
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'w') as archivo:
        archivo.write(nuevo_contenido)
