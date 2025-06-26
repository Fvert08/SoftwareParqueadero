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
# Encriptación y desencriptación de archivos con una clave personalizada
import os
import hashlib
import base64

# Palabra clave incrustada en el código (cámbiala por la que quieras)

def generar_clave_desde_palabra(palabra_clave):
    """Genera una clave hash basada en la palabra clave."""
    # Usamos SHA-256 para crear un hash de 32 bytes desde la palabra clave
    return hashlib.sha256(palabra_clave.encode()).digest()

def expandir_clave(clave, longitud):
    """Expande la clave para que sea al menos tan larga como el mensaje."""
    clave_expandida = b''
    while len(clave_expandida) < longitud:
        clave_expandida += clave
    return clave_expandida[:longitud]

def encriptar(mensaje):
    palabra_clave = "Parqueadero2025"  # Palabra clave incrustada en el código
    """Encripta un mensaje usando XOR con la palabra clave."""
    # Convertir mensaje a bytes
    mensaje_bytes = mensaje.encode('utf-8')
    
    # Generar clave hash
    clave = generar_clave_desde_palabra(palabra_clave)
    
    # Expandir la clave para que coincida con la longitud del mensaje
    clave_expandida = expandir_clave(clave, len(mensaje_bytes))
    
    # Aplicar XOR
    resultado = bytearray()
    for i in range(len(mensaje_bytes)):
        resultado.append(mensaje_bytes[i] ^ clave_expandida[i])
    
    # Convertir a base64 para poder guardarlo como texto
    return base64.b64encode(resultado).decode('utf-8')

def desencriptar(mensaje_encriptado):
    """Desencripta un mensaje usando XOR con la palabra clave."""
    palabra_clave = "Parqueadero2025"
    try:
        # Decodificar desde base64
        mensaje_bytes = base64.b64decode(mensaje_encriptado.encode('utf-8'))
        
        # Generar la misma clave hash
        clave = generar_clave_desde_palabra(palabra_clave)
        
        # Expandir la clave
        clave_expandida = expandir_clave(clave, len(mensaje_bytes))
        
        # Aplicar XOR (la misma operación desencripta)
        resultado = bytearray()
        for i in range(len(mensaje_bytes)):
            resultado.append(mensaje_bytes[i] ^ clave_expandida[i])
        
        # Convertir de vuelta a string
        return resultado.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error al desencriptar: {e}")

def leer_archivoDesencriptado(carpeta, nombre_archivo):
    """Lee un archivo y desencripta su contenido."""
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as archivo:
            contenido_encriptado = archivo.read().strip()
        return desencriptar(contenido_encriptado)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_completa}")
    except Exception as e:
        raise ValueError(f"Error al leer o desencriptar el archivo: {e}")

def escribir_archivoEncriptado(carpeta, nombre_archivo, nuevo_contenido):
    """Encripta el contenido y lo guarda en el archivo."""
    # Crear carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    contenido_encriptado = encriptar(nuevo_contenido)
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    
    with open(ruta_completa, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido_encriptado)

def verificar_archivos_config():
    """Verifica si los archivos de configuración existen, si no los crea."""
    archivos_config = ['VH.txt', 'VD.txt', 'VM.txt']
    carpeta_config = 'config'
    
    # Crear carpeta config si no existe
    if not os.path.exists(carpeta_config):
        os.makedirs(carpeta_config)
        print(f"Carpeta '{carpeta_config}' creada.")
    
    archivos_faltantes = []
    for archivo in archivos_config:
        ruta_completa = os.path.join(carpeta_config, archivo)
        if not os.path.exists(ruta_completa):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"Archivos faltantes encontrados: {archivos_faltantes}")
        print("Creando archivos de configuración...")
        for archivo in archivos_faltantes:
            escribir_archivoEncriptado(carpeta_config, archivo, '0')
        print("Archivos de configuración creados y encriptados.")
    else:
        print("Todos los archivos de configuración ya existen.")

# Función de prueba para verificar que funciona
def probar_encriptacion():
    """Prueba las funciones de encriptación y desencriptación."""
    mensaje_prueba = "Hola, este es un mensaje de prueba con caracteres especiales: ñáéíóú"
    print(f"Mensaje original: {mensaje_prueba}")
    
    # Encriptar
    mensaje_encriptado = encriptar(mensaje_prueba)
    print(f"Mensaje encriptado: {mensaje_encriptado}")
    
    # Desencriptar
    mensaje_desencriptado = desencriptar(mensaje_encriptado)
    print(f"Mensaje desencriptado: {mensaje_desencriptado}")
    
    # Verificar que son iguales
    if mensaje_prueba == mensaje_desencriptado:
        print("✅ Encriptación funcionando correctamente!")
    else:
        print("❌ Error en la encriptación")

# Uso principal
if __name__ == "__main__":
    PALABRA_CLAVE = "Parqueadero2025"  # Palabra clave incrustada en el código
    print("Sistema de encriptación personalizado iniciado")
    print(f"Usando palabra clave incrustada: {'*' * len(PALABRA_CLAVE)}")
    
    # Verificar y crear archivos de configuración
    verificar_archivos_config()
    
    # Prueba opcional del sistema
    print("\n--- Prueba del sistema ---")
    probar_encriptacion()
    
    # Ejemplo de uso con archivos
    print("\n--- Prueba con archivos ---")
    try:
        # Leer un archivo (ejemplo)
        contenido = leer_archivoDesencriptado('config', 'VH.txt')
        print(f"Contenido de VH.txt: {contenido}")
        
        # Escribir nuevo contenido
        escribir_archivoEncriptado('config', 'prueba.txt', 'Este es un archivo de prueba encriptado')
        print("Archivo prueba.txt creado y encriptado")
        
        # Leer el archivo recién creado
        contenido_prueba = leer_archivoDesencriptado('config', 'prueba.txt')
        print(f"Contenido de prueba.txt: {contenido_prueba}")
        
    except Exception as e:
        print(f"Error: {e}")