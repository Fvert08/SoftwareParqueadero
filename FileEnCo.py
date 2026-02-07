import datetime  # Importamos el módulo completo para que funcione datetime.now()

def generarCodigoEncriptado(palabra, fecha_str, iteraciones):
    # Usamos la ruta completa al método strptime dentro del módulo
    fecha_actual = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
    
    ano = fecha_actual.year
    mes = fecha_actual.month
    dia = fecha_actual.day

    def asegurar_letra_y_numero(s):
        if not any(c.isalpha() for c in s):
            s = s[:-1] + 'a'
        if not any(c.isdigit() for c in s):
            s = s[:-1] + '1'
        return s

    def mezclar_cadena(codigo, dia):
        resultado = list(codigo)
        for i in range(3):
            if dia % 2 == 0:
                resultado[i], resultado[i + 8] = resultado[i + 8], resultado[i]
            else:
                resultado[i + 4], resultado[i + 8] = resultado[i + 8], resultado[i + 4]
        return ''.join(resultado)

    def operar_caracteres(c1, c2, iteraciones_restantes, fecha_char):
        suma = (ord(c1) + ord(c2) + iteraciones_restantes + ord(fecha_char)) % 36
        if suma < 10:
            return chr(suma + ord('0'))
        else:
            return chr(suma - 10 + ord('a'))

    def encriptar(palabra, iteraciones_restantes):
        if iteraciones_restantes == 0:
            return palabra

        valores_ascii = [ord(char) for char in palabra]
        suma_valores = sum(valores_ascii) + ano + mes + dia
        
        longitud = len(valores_ascii) if len(valores_ascii) > 0 else 1
        division_entera = suma_valores // longitud
        resto = suma_valores % longitud

        parte1 = f"{hex(division_entera)[-3:]}".replace('x', 'a')
        parte2 = f"{oct(resto * 3)[-3:]}".replace('o', 'b')
        parte3 = f"{hex(resto * 17)[-3:]}".replace('x', 'c')

        parte1 = asegurar_letra_y_numero(parte1.zfill(3))
        parte2 = asegurar_letra_y_numero(parte2.zfill(3))
        parte3 = asegurar_letra_y_numero(parte3.zfill(3))

        codigo_base = f"{parte1}-{parte2}-{parte3}"
        codigo_mezclado = mezclar_cadena(codigo_base, dia)

        partes = codigo_mezclado.split('-')
        nueva_parte1 = ''.join(operar_caracteres(partes[0][i], partes[2][i], iteraciones_restantes, fecha_str[i % len(fecha_str)]) for i in range(3))
        nueva_parte2 = ''.join(operar_caracteres(partes[1][i], partes[0][i], iteraciones_restantes, fecha_str[(i + 3) % len(fecha_str)]) for i in range(3))
        nueva_parte3 = ''.join(operar_caracteres(partes[2][i], partes[1][i], iteraciones_restantes, fecha_str[(i + 6) % len(fecha_str)]) for i in range(3))

        nuevo_codigo = f"{nueva_parte1}-{nueva_parte2}-{nueva_parte3}"
        return encriptar(nuevo_codigo, iteraciones_restantes - 1)

    return encriptar(palabra, iteraciones)

# --- PARTE INFERIOR IDENTICA A TU SOLICITUD ---
if __name__ == "__main__":
    fecha_str = datetime.datetime.now().strftime('%Y-%m-%d')
    fecha_actual = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
    dia = fecha_actual.day
    codigo = generarCodigoEncriptado("parqueaderola18", str(fecha_str), int(dia))
    print("Código generado:", codigo)