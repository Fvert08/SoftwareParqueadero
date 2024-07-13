from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter

# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketIngresoMoto(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado):
    # Dimensiones típicas de un recibo POS, aumentadas para mejorar calidad
    width, height = 430, 620  # Aumentar el tamaño para mejorar la calidad de impresión
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
    d.text((90, 184), f"TICKET DE ENTRADA", font=font_bold, fill='black')
    d.text((20, 200), f"-------------------------------------------------", font=font_bold, fill='black')
    
    font = ImageFont.truetype("arial.ttf", 24)
    d.text((20, 220), f"Placa: {Placa}", font=font_bold, fill='black')
    d.text((20, 240), f"Cascos: {Cascos}", font=font_bold, fill='black')
    d.text((20, 260), f"Casillero: {Casillero}", font=font_bold, fill='black')
    d.text((20, 280), f"Fecha: {Fecha}", font=font_bold, fill='black')
    d.text((20, 300), f"Hora: {Hora}", font=font_bold, fill='black')
    
    # Generar código de barras
    cod_barra = barcode.get_barcode_class('code128')
    codigo = cod_barra(codigo_barras, writer=ImageWriter())
    # Configurar la resolución del código de barras
    barcode_opts = {'module_height': 15.0, 'module_width': 0.4, 'font_size': 10, 'text_distance': 5.0, 'quiet_zone': 1.0}
    codigo_img = codigo.save('codigo_barras', options=barcode_opts)
    # Cargar y colocar el código de barras en la imagen
    codigo_barra = Image.open('codigo_barras.png')
    codigo_barra = codigo_barra.resize((400, 200), Image.LANCZOS)
    img.paste(codigo_barra, (10, 340))
    # Información restante
    font = ImageFont.truetype("arial.ttf", 14)
    d.text((120, 515), f"Valor hora o fracción: $1.000", font=font, fill='black')
    d.text((95, 535), f"Lunes a sabado: De 6 a.m. a 10 p.m.", font=font, fill='black')
    d.text((90, 555), f"Domingos y festivos: de 7 a.m. a 6 p.m.", font=font, fill='black')
    d.text((40, 575), f"SI PIERDE ESTE TICKET TENDRA QUE PRESENTAR ", font=font, fill='black')
    d.text((40, 595), f"LA TARJETA DE PROPIEDAD DE SU MOTO", font=font, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)

    print(f"Recibo generado y guardado en: {ruta_guardado}")

# Ejemplo de uso
Placa = "ABC12C"
Cascos = "2"
Casillero = "4"
Fecha = "13-07-2024"
Hora = "10:17:00"
codigo_barras = "0001"
ruta_logo = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\Logo.png"
ruta_guardado = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\TicketIngresoMoto.png"

generarTicketIngresoMoto(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado)
