from leerTxt import leer_archivo
DB_CONFIG = {
    'host': leer_archivo('config','host.txt'),
    'user': leer_archivo('config','user.txt'),
    'password': leer_archivo('config','password.txt'),
    'database': leer_archivo('config','database.txt'),
    'port': int(leer_archivo('config','port.txt'))  # Convertir a entero
}
