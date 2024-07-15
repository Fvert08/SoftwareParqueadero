from PIL import Image, ImageDraw, ImageFont

# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketSalidaMoto(FechaIngreso,FechaSalida,HoraIngreso,HoraSalida,TiempoTotal,TotalAPagar,Placa,Casillero, ruta_logo, ruta_guardado):
    width, height = 1720, 2200  # Cuadruplicar el tamaño original para mejorar la calidad de impresión
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Cargar y redimensionar el logo
    logo = Image.open(ruta_logo)
    logo = logo.resize((560, 560), Image.LANCZOS)

    # Colocar el logo al inicio del recibo
    img.paste(logo, (80, 80))

    # Configurar fuentes
    font = ImageFont.truetype("arial.ttf", 80)  # Cuadruplicar tamaño de fuente
    font_bold = ImageFont.truetype("arialbd.ttf", 96)
    
    # Datos del parqueadero
    d.text((740, 80), f"PARQUEADERO LA 18", font=font, fill='black')
    d.text((720, 160), f"----------------------------", font=font_bold, fill='black')
    d.text((740, 240), f"Teléfono: 3192742428", font=font, fill='black')
    d.text((740, 320), f"Calle si #01-02", font=font, fill='black')
    d.text((840, 400), f"Pereira", font=font, fill='black')
    d.text((720, 480), f"----------------------------", font=font_bold, fill='black')
    
    # Datos del J Dev
    font = ImageFont.truetype("arial.ttf", 48)
    d.text((768, 560), f"Desarrollado por J DEV.", font=font, fill='black')
    d.text((768, 624), f"Contacto: 3192742428 - 3246844088", font=font, fill='black')
    
    # Datos del Ticket
    font = ImageFont.truetype("arial.ttf", 120)
    d.text((80, 640), f"-------------------------------------------------", font=font_bold, fill='black')
    d.text((360, 736), f"TICKET DE SALIDA", font=font_bold, fill='black')
    d.text((80, 800), f"------------------------------------------------", font=font_bold, fill='black')
    font = ImageFont.truetype("arial.ttf", 96)
    d.text((640, 880), f"INGRESO", font=font_bold, fill='black')
    d.text((80, 1040), f"Fecha: {FechaIngreso}", font=font_bold, fill='black')
    d.text((80, 1120), f"Hora: {HoraIngreso}", font=font_bold, fill='black')
    d.text((80, 1200), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((640, 1280), f"SALIDA", font=font_bold, fill='black')
    d.text((80, 1440), f"Fecha: {FechaSalida}", font=font_bold, fill='black')
    d.text((80, 1520), f"Hora: {HoraSalida}", font=font_bold, fill='black')
    d.text((80, 1600), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((320, 1680), f"Tiempo total: {TiempoTotal}", font=font_bold, fill='black')
    d.text((80, 1760), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((320, 1840), f"Total a pagar: {TotalAPagar}", font=font_bold, fill='black')
    d.text((80, 1920), f"------------------------------------------------", font=font_bold, fill='black')
    # Información restante
    font = ImageFont.truetype("arial.ttf", 68)
    d.text((80, 2000), f"Placa: {Placa}    |", font=font, fill='black')
    d.text((720, 2000), f"Casillero: {Casillero}", font=font, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    print(f"Recibo de salida generado")

# Ejemplo de uso
Placa = "ABC12C"
Cascos = "2"
Casillero = "4"
FechaIngreso = "13-07-2024"
FechaSalida = "13-07-2024"
HoraIngreso = "10:10:00"
HoraSalida= "10:17:00"
TiempoTotal = "00:07:00"
TotalAPagar = "$1.000"
ruta_logo = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\Logo.png"
ruta_guardado = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\TicketSalidaMoto.png"

generarTicketSalidaMoto(FechaIngreso,FechaSalida,HoraIngreso,HoraSalida,TiempoTotal,TotalAPagar,Placa,Casillero, ruta_logo, ruta_guardado)
