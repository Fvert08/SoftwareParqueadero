from PIL import Image, ImageDraw, ImageFont
import os
import win32print
import win32ui
from PIL import ImageWin
# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketSalidaMoto(FechaIngreso,FechaSalida,HoraIngreso,HoraSalida,TiempoTotal,TotalAPagar,Placa,Casillero):
    width, height = 1720, 2080  # Cuadruplicar el tamaño original para mejorar la calidad de impresión
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_logo = os.path.join(directorio_actual, "..","imagenes","Logo.png")
    ruta_guardado = os.path.join(directorio_actual, "..","Tickets","TicketSalidaMoto.png")
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
    d.text((320, 1840), f"Total: ${int(TotalAPagar):,.0f}", font=font, fill='black')
    d.text((80, 1920), f"------------------------------------------------", font=font_bold, fill='black')
    # Información restante
    font = ImageFont.truetype("arial.ttf", 68)
    d.text((80, 2000), f"Placa: {Placa}    |", font=font, fill='black')
    d.text((720, 2000), f"Casillero: {Casillero}", font=font, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    imprimirTicket(ruta_guardado)
    print(f"Recibo de salida generado")

def mm_to_pixels(mm, dpi):
    return int((mm / 25.4) * dpi)
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
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("TicketSalidaMoto", None, "RAW"))
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
                hDC.StartDoc("TicketSalidaMoto")
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