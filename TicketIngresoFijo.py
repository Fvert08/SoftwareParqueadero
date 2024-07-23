from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import os
import win32print
import win32ui
from PIL import ImageWin
def mm_to_pixels(mm, dpi):
    return int((mm / 25.4) * dpi)
# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketIngresoFijo(Fecha, Hora,Tipo,Nota,Valor):
    # Obtener la ruta del directorio actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_logo = os.path.join(directorio_actual, "Logo.png")
    ruta_guardado = os.path.join(directorio_actual, "TicketIngresoFijo.png")
    codigo_barras = "0001"
    # Dimensiones típicas de un recibo POS, aumentadas para mejorar calidad
    width, height = 1720, 2220  # Duplicar el tamaño original nuevamente para mejorar la calidad de impresión
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Cargar y redimensionar el logo
    logo = Image.open(ruta_logo)
    logo = logo.resize((560, 560), Image.LANCZOS)

    # Colocar el logo al inicio del recibo
    img.paste(logo, (80, 80))

    # Configurar fuentes
    font = ImageFont.truetype("arial.ttf", 80)  # Duplicar tamaño de fuente nuevamente
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
    d.text((360, 736), f"TICKET DE ENTRADA", font=font_bold, fill='black')
    d.text((80, 800), f"-------------------------------------------------", font=font_bold, fill='black')
    
    font = ImageFont.truetype("arial.ttf", 96)
    d.text((80, 880), f"Fecha: {Fecha}", font=font_bold, fill='black')
    d.text((80, 960), f"Hora: {Hora}", font=font_bold, fill='black')
    d.text((80, 1040), f"Tipo: {Tipo}", font=font_bold, fill='black')
    d.text((80, 1120), f"Nota: {Nota}", font=font_bold, fill='black')
    d.text((80, 1200), f"Valor: {Valor}", font=font_bold, fill='black')
    
    # Generar código de barras
    cod_barra = barcode.get_barcode_class('code128')
    codigo = cod_barra(codigo_barras, writer=ImageWriter())
    # Configurar la resolución del código de barras
    barcode_opts = {'module_height': 60.0, 'module_width': 1.6, 'font_size': 40, 'text_distance': 20.0, 'quiet_zone': 4.0}
    codigo_img = codigo.save('codigo_barras', options=barcode_opts)
    # Cargar y colocar el código de barras en la imagen
    codigo_barra = Image.open('codigo_barras.png')
    codigo_barra = codigo_barra.resize((1600, 800), Image.LANCZOS)
    img.paste(codigo_barra, (40, 1360))
    # Información restante
    font = ImageFont.truetype("arial.ttf", 56)
    d.text((380, 2060), f"Lunes a sabado: De 6 a.m. a 10 p.m.", font=font, fill='black')
    d.text((360, 2140), f"Domingos y festivos: de 7 a.m. a 6 p.m.", font=font, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    print(f"Recibo Fijo generado y guardado en: {ruta_guardado}")
    imprimirTicket(ruta_guardado)

# Función para imprimir el recibo
def imprimirTicket(ruta_archivo):
    try:
        # Obtener el nombre de la impresora predeterminada
        impresora_predeterminada = win32print.GetDefaultPrinter()
        print(f"Impresora predeterminada: {impresora_predeterminada}")

        # Supongamos una resolución de impresora de 203 DPI
        dpi = 203
        paper_width_mm = 70  # Ajustar a 70mm para hacer la imagen más pequeña
        paper_width_px = mm_to_pixels(paper_width_mm, dpi)

        # Abrir la impresora
        hPrinter = win32print.OpenPrinter(impresora_predeterminada)
        try:
            # Crear un trabajo de impresión
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("TicketIngresoFijo", None, "RAW"))
            try:
                win32print.StartPagePrinter(hPrinter)
                
                # Cargar la imagen
                bmp = Image.open(ruta_archivo)
                bmp = bmp.resize((paper_width_px, int(bmp.height * (paper_width_px / bmp.width))), Image.LANCZOS)
                dib = ImageWin.Dib(bmp)
                
                # Obtener el contexto de dispositivo
                hDC = win32ui.CreateDC()
                hDC.CreatePrinterDC(impresora_predeterminada)
                
                # Ajustar el tamaño de la imagen al tamaño del papel
                hDC.StartDoc("TicketIngresoFijo")
                hDC.StartPage()
                dib.draw(hDC.GetHandleOutput(), (0, 0, bmp.size[0], bmp.size[1]))
                hDC.EndPage()
                hDC.EndDoc()
                
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
        print("Impresión enviada correctamente.")
    except Exception as e:
        print(f"Error al intentar imprimir: {e}")