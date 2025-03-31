import os
from cryptography.fernet import Fernet
import os



#----------------Lectura y escritura de archivos (Normal)------------------
def leer_archivo(carpeta, nombre_archivo):
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'r') as archivo:
        return archivo.read().strip()
def escribir_archivo (carpeta, nombre_archivo,nuevo_contenido):
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'w') as archivo:
        archivo.write(nuevo_contenido)

#----------------Lectura y escritura de archivos (Encriptado)------------------
def generar_clave():
    """Genera una clave y la guarda en un archivo."""
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(clave)

def cargar_clave():
    """Carga la clave desde el archivo."""
    return open("clave.key", "rb").read()

def encriptar(mensaje, clave):
    """Encripta un mensaje con la clave dada."""
    f = Fernet(clave)
    return f.encrypt(mensaje.encode()).decode()

def desencriptar(mensaje_encriptado, clave):
    """Desencripta un mensaje con la clave dada."""
    f = Fernet(clave)
    return f.decrypt(mensaje_encriptado.encode()).decode()

def leer_archivoDesencriptado(carpeta, nombre_archivo):
    """Lee un archivo y desencripta su contenido."""
    clave = cargar_clave()
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'r') as archivo:
        contenido_encriptado = archivo.read().strip()
    return desencriptar(contenido_encriptado, clave)

def escribir_archivoEncriptado(carpeta, nombre_archivo, nuevo_contenido):
    """Encripta el contenido y lo guarda en el archivo."""
    clave = cargar_clave()
    contenido_encriptado = encriptar(nuevo_contenido, clave)
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    with open(ruta_completa, 'w') as archivo:
        archivo.write(contenido_encriptado)
#generar clave
def clave_existe():
    return os.path.exists("clave.key")
# Uso
if clave_existe():
    print("La clave ya existe.")
else:
    print("No se encontró clave.key, generando una nueva...")
    generar_clave()
    escribir_archivoEncriptado('config','VH.txt','0')
    escribir_archivoEncriptado('config','VD.txt','0')
    escribir_archivoEncriptado('config','VM.txt','0')