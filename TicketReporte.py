from PIL import Image, ImageDraw, ImageFont

# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketReporte(Tipo, FechaInicio, FechaFin,Registros,DineroTotal, Fecha, Hora, ruta_logo, ruta_guardado):
    # Dimensiones típicas de un recibo POS, cuadruplicadas para mejorar calidad
    width, height = 1720, 1760  # Cuadruplicar el tamaño original para mejorar la calidad de impresión
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
    d.text((360, 736), f"TICKET DE REPORTE", font=font_bold, fill='black')
    d.text((80, 800), f"------------------------------------------------", font=font_bold, fill='black')
    font = ImageFont.truetype("arial.ttf", 96)
    d.text((80, 880), f"Numero de reporte: 1", font=font_bold, fill='black')
    d.text((80, 960), f"Fecha de generación: {Fecha}", font=font_bold, fill='black')
    d.text((80, 1040), f"Hora de generación: {Hora}", font=font_bold, fill='black')
    d.text((80, 1120), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((80, 1200), f"Reportar: {Tipo}", font=font_bold, fill='black')
    d.text((80, 1280), f"Fecha inicio: {FechaInicio}", font=font_bold, fill='black')
    d.text((80, 1360), f"Fecha fin: {FechaFin}", font=font_bold, fill='black')
    d.text((80, 1440), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((80, 1520), f"Total de registros: {Registros}", font=font_bold, fill='black')
    d.text((80, 1600), f"Dinero total: {DineroTotal}", font=font_bold, fill='black')
    d.text((80, 1680), f"------------------------------------------------", font=font_bold, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    print(f"Ticket de reporte generado")

# Ejemplo de uso
Tipo = "Todo"
FechaInicio="13-07-2024"
FechaFin = "13-07-2024"
Registros = "100"
DineroTotal = "$100.000"
Fecha = "13-07-2024"
Hora = "10:17:00"
ruta_logo = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\Logo.png"
ruta_guardado = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\TicketReporte.png"

generarTicketReporte(Tipo, FechaInicio, FechaFin,Registros,DineroTotal, Fecha, Hora, ruta_logo, ruta_guardado)
