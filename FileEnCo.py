import datetime

def generarCodigoEncriptado(palabra, fecha_str, iteraciones):
    # Convertir la cadena de fecha a un objeto datetime
    fecha_actual = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
    # Obtener año, mes y día
    ano = fecha_actual.year
    mes = fecha_actual.month
    dia = fecha_actual.day

    # Función para asegurar que una cadena tenga al menos una letra y un número
    def asegurar_letra_y_numero(s):
        if not any(c.isalpha() for c in s):
            s = s[:-1] + 'a'  # Reemplazar el último carácter por una letra si no hay letras
        if not any(c.isdigit() for c in s):
            s = s[:-1] + '1'  # Reemplazar el último carácter por un número si no hay números
        return s

    # Función para mezclar los caracteres de una cadena en base a la paridad del día
    def mezclar_cadena(codigo, dia):
        partes = codigo.split('-')
        resultado = list(codigo)

        for i in range(3):  # Iterar sobre cada posición de los tres caracteres
            if dia % 2 == 0:
                resultado[i], resultado[i + 8] = resultado[i + 8], resultado[i]  # Mezcla con la tercera sección
            else:
                resultado[i + 4], resultado[i + 8] = resultado[i + 8], resultado[i + 4]  # Mezcla con la segunda sección

        return ''.join(resultado)

    # Función para realizar operaciones entre caracteres y asegurar que el resultado sea un carácter alfanumérico
    def operar_caracteres(c1, c2, iteraciones_restantes, fecha_char):
        suma = (ord(c1) + ord(c2) + iteraciones_restantes + ord(fecha_char)) % 36  # Suma y módulo 36 para asegurar que el resultado esté en el rango alfanumérico
        if suma < 10:
            return chr(suma + ord('0'))  # Convertir a dígito
        else:
            return chr(suma - 10 + ord('a'))  # Convertir a letra

    def encriptar(palabra, iteraciones_restantes):
        if iteraciones_restantes == 0:
            return palabra

        # Convertir la palabra a una lista de números basada en sus caracteres ASCII
        valores_ascii = [ord(char) for char in palabra]

        # Realizar operaciones matemáticas y de conversión
        suma_valores = sum(valores_ascii) + ano + mes + dia
        division_entera = suma_valores // len(valores_ascii)
        resto = suma_valores % len(valores_ascii)

        # Crear partes del código con operaciones adicionales para mayor complejidad
        parte1 = f"{hex(division_entera)[-3:]}".replace('x', 'a')  # Convertir a hexadecimal y asegurar una letra
        parte2 = f"{oct(resto * 3)[-3:]}".replace('o', 'b')  # Convertir a octal y asegurar una letra
        parte3 = f"{hex(resto * 17)[-3:]}".replace('x', 'c')  # Convertir a hexadecimal y asegurar una letra

        # Normalizar y asegurar que cada parte tiene al menos una letra y un número
        parte1 = asegurar_letra_y_numero(parte1.zfill(3))
        parte2 = asegurar_letra_y_numero(parte2.zfill(3))
        parte3 = asegurar_letra_y_numero(parte3.zfill(3))

        # Crear el código en el formato especificado
        codigo = f"{parte1}-{parte2}-{parte3}"

        # Mezclar los caracteres del código
        codigo = mezclar_cadena(codigo, dia)

        # Realizar operaciones entre los caracteres de cada sección para mayor complejidad
        partes = codigo.split('-')
        nueva_parte1 = ''.join(operar_caracteres(partes[0][i], partes[2][i], iteraciones_restantes, fecha_str[i % len(fecha_str)]) for i in range(3))
        nueva_parte2 = ''.join(operar_caracteres(partes[1][i], partes[0][i], iteraciones_restantes, fecha_str[(i + 3) % len(fecha_str)]) for i in range(3))
        nueva_parte3 = ''.join(operar_caracteres(partes[2][i], partes[1][i], iteraciones_restantes, fecha_str[(i + 6) % len(fecha_str)]) for i in range(3))

        # Crear el nuevo código con las partes operadas
        nuevo_codigo = f"{nueva_parte1}-{nueva_parte2}-{nueva_parte3}"

        # Llamada recursiva
        return encriptar(nuevo_codigo, iteraciones_restantes - 1)

    return encriptar(palabra, iteraciones)

# Ejemplo de uso
palabra = "parqueaderola18"
fecha_str = "2024-04-11"
iteraciones = 1
codigo_encriptado = generarCodigoEncriptado(palabra, fecha_str, iteraciones)
print(codigo_encriptado)
