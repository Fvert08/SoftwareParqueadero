from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter

# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketSalidaMoto(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado):
    # Dimensiones típicas de un recibo POS, aumentadas para mejorar calidad
    width, height = 430, 550  # Aumentar el tamaño para mejorar la calidad de impresión
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
    d.text((90, 184), f"TICKET DE SALIDA", font=font_bold, fill='black')
    d.text((20, 200), f"------------------------------------------------", font=font_bold, fill='black')
    font = ImageFont.truetype("arial.ttf", 24)
    d.text((160, 220), f"INGRESO", font=font_bold, fill='black')
    d.text((20, 260), f"Fecha: {Fecha}", font=font_bold, fill='black')
    d.text((20, 280), f"Hora: {Hora}", font=font_bold, fill='black')
    d.text((20, 300), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((160,320), f"SALIDA", font=font_bold, fill='black')
    d.text((20, 360), f"Fecha: {Fecha}", font=font_bold, fill='black')
    d.text((20, 380), f"Hora: {Hora}", font=font_bold, fill='black')
    d.text((20, 400), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((80,420), f"Tiempo total: {Hora}", font=font_bold, fill='black')
    d.text((20, 440), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((80,460), f"Total a pagar: $1.000", font=font_bold, fill='black')
    d.text((20, 480), f"------------------------------------------------", font=font_bold, fill='black')
    # Información restante
    font = ImageFont.truetype("arial.ttf", 17)
    d.text((20, 500), f"Placa: ABC12C    |", font=font, fill='black')
    d.text((180, 500), f"Casillero: 2", font=font, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    print(f"Recibo de salida generado")

# Ejemplo de uso
Placa = "ABC12C"
Cascos = "2"
Casillero = "4"
Fecha = "13-07-2024"
Hora = "10:17:00"
codigo_barras = "0001"
ruta_logo = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\Logo.png"
ruta_guardado = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\TicketSalidaMoto.png"

generarTicketSalidaMoto(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado)
