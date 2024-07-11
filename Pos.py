from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter

# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generar_recibo_pos(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado):
    # Dimensiones típicas de un recibo POS
    width, height = 230, 620
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Cargar y redimensionar el logo
    logo = Image.open(ruta_logo)
    logo = logo.resize((150, 150))

    # Colocar el logo al inicio del recibo
    img.paste(logo, (40, 10))  # Ajustar posición del logo para que haya más espacio debajo del logo antes de comenzar a escribir el texto

    # Configurar fuentes
    font = ImageFont.truetype("arial.ttf", 12)
    font_bold = ImageFont.truetype("arialbd.ttf", 12)

    # Escribir texto en la imagen debajo del logo
    d.text((10, 170), f"PARQUEADERO SISISI", font=font, fill='black')
    d.text((10, 190), f"-------------------", font=font_bold, fill='black')
    d.text((10, 210), f"Telefono: 3192742428", font=font, fill='black')
    d.text((10, 230), f"Calle pene #01-02", font=font, fill='black')
    d.text((10, 250), f"Pereira", font=font, fill='black')
    d.text((10, 270), f"-------------------", font=font_bold, fill='black')
    d.text((10, 290), f"TICKET DE ENTRADA", font=font_bold, fill='black')
    d.text((10, 310), f"-------------------", font=font_bold, fill='black')
    d.text((10, 330), f"Placa: {Placa}", font=font_bold, fill='black')
    d.text((10, 350), f"Cascos: {Cascos}", font=font_bold, fill='black')
    d.text((10, 370), f"Casillero: {Casillero}", font=font_bold, fill='black')
    d.text((10, 390), f"Fecha: {Fecha}", font=font_bold, fill='black')
    d.text((10, 410), f"Hora: {Hora}", font=font_bold, fill='black')

    # Generar código de barras
    cod_barra = barcode.get_barcode_class('code128')
    codigo = cod_barra(codigo_barras, writer=ImageWriter())
    codigo_img = codigo.save('codigo_barras')

    # Cargar y colocar el código de barras en la imagen
    codigo_barra = Image.open('codigo_barras.png')
    codigo_barra = codigo_barra.resize((250, 150))
    img.paste(codigo_barra, (1, 430))

    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)

    print(f"Recibo generado y guardado en: {ruta_guardado}")

# Ejemplo de uso
Placa = "ABC12C"
Cascos = "2"
Casillero = "4"
Fecha = "11-07-2024"
Hora = "9:45:00"
codigo_barras = "0001"
ruta_logo = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\Logo.png"
ruta_guardado = r"C:\Users\Impor\OneDrive\Escritorio\Parqueadero\SoftwareParqueadero\recibo_pos_con_logo.png"

generar_recibo_pos(Placa, Cascos, Casillero, Fecha, Hora, codigo_barras, ruta_logo, ruta_guardado)
