from PIL import Image, ImageDraw, ImageFont
# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketSalidaMoto(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado):
    # Dimensiones típicas de un recibo POS, aumentadas para mejorar calidad
    width, height = 430, 450  # Aumentar el tamaño para mejorar la calidad de impresión
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Cargar y redimensionar el logo
    logo = Image.open(ruta_logo)
    logo = logo.resize((140, 140), Image.LANCZOS)

    # Colocar el logo al inicio del recibo
    img.paste(logo, (20, 20))

    # Configurar fuentes
    font = ImageFont.truetype("arial.ttf", 20)  # Aumentar tamaño de fuente
    font_bold = ImageFont.truetype("arialbd.ttf", 24)
    
    # Datos del parqueadero
    d.text((185, 20), f"PARQUEADERO LA 18", font=font, fill='black')
    d.text((180, 40), f"----------------------------", font=font_bold, fill='black')
    d.text((185, 60), f"Teléfono: 3192742428", font=font, fill='black')
    d.text((185, 80), f"Calle si #01-02", font=font, fill='black')
    d.text((210, 100), f"Pereira", font=font, fill='black')
    d.text((180, 120), f"----------------------------", font=font_bold, fill='black')
    
    # Datos del J Dev
    font = ImageFont.truetype("arial.ttf", 12)
    d.text((192, 140), f"Desarrollado por J DEV.", font=font, fill='black')
    d.text((192, 156), f"Contacto: 3192742428 - 3246844088", font=font, fill='black')
    
    # Datos del Ticket
    font = ImageFont.truetype("arial.ttf", 30)
    d.text((20, 160), f"-------------------------------------------------", font=font_bold, fill='black')
    d.text((90, 184), f"TICKET DE REPORTE", font=font_bold, fill='black')
    d.text((20, 200), f"------------------------------------------------", font=font_bold, fill='black')
    font = ImageFont.truetype("arial.ttf", 24)
    d.text((20, 220), f"Numero de reporte: 1", font=font_bold, fill='black')
    d.text((20, 240), f"Fecha de generación: {Fecha}", font=font_bold, fill='black')
    d.text((20, 260), f"Hora de generación: {Hora}", font=font_bold, fill='black')
    d.text((20, 280), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((20, 300), f"Reportar: Todo", font=font_bold, fill='black')
    d.text((20, 320), f"Fecha inicio: {Fecha}", font=font_bold, fill='black')
    d.text((20, 340), f"Fecha fin: {Fecha}", font=font_bold, fill='black')
    d.text((20, 360), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((20,380), f"Total de registros: 100", font=font_bold, fill='black')
    d.text((20,400), f"Dinero total: $100.000", font=font_bold, fill='black')
    d.text((20, 420), f"------------------------------------------------", font=font_bold, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    print(f"Ticket de reporte generado")

# Ejemplo de uso
Placa = "ABC12C"
Cascos = "2"
Casillero = "4"
Fecha = "13-07-2024"
Hora = "10:17:00"
codigo_barras = "0001"
ruta_logo = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\Logo.png"
ruta_guardado = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\TicketReporte.png"

generarTicketSalidaMoto(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado)