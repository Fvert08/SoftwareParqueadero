from PIL import Image, ImageDraw, ImageFont
import os
import win32print
import win32ui
from PIL import ImageWin
def mm_to_pixels(mm, dpi):
    return int((mm / 25.4) * dpi)
# Función para generar y guardar el recibo como imagen con dimensiones de POS y logo
def generarTicketReporteCompleto(codigo,Tipo,Fecha, Hora,FechaInicio, FechaFin,registrosMotosHora,dineroTotalMotosHora,registrosMotosDia,dineroTotalMotosDia, registrosMotosMes,dineroTotalMotosMes,registrosFijos,dineroTotalFijos):
    
    # Obtener la ruta del directorio actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    ruta_logo = os.path.join(directorio_actual, "Logo.png")
    ruta_guardado = os.path.join(directorio_actual, "TicketReporteCompleto.png")
    # Dimensiones típicas de un recibo POS, cuadruplicadas para mejorar calidad
    width, height = 1720, 2720 # Cuadruplicar el tamaño original para mejorar la calidad de impresión
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
    d.text((80, 880), f"Numero de reporte: {codigo}", font=font_bold, fill='black')
    d.text((80, 960), f"Fecha de generación: {Fecha}", font=font_bold, fill='black')
    d.text((80, 1040), f"Hora de generación: {Hora}", font=font_bold, fill='black')
    d.text((80, 1120), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((80, 1200), f"Reportar: {Tipo}", font=font_bold, fill='black')
    d.text((80, 1280), f"Fecha inicio: {FechaInicio}", font=font_bold, fill='black')
    d.text((80, 1360), f"Fecha fin: {FechaFin}", font=font_bold, fill='black')
    d.text((80, 1440), f"------------------------------------------------", font=font_bold, fill='black')
    d.text((80, 1520), f"Motos hora: {registrosMotosHora}", font=font_bold, fill='black')
    d.text((80, 1600), f"Total: {dineroTotalMotosHora}", font=font_bold, fill='black')

    d.text((80, 1760), f"Motos dia: {registrosMotosDia}", font=font_bold, fill='black')
    d.text((80, 1840), f"Total: {dineroTotalMotosDia}", font=font_bold, fill='black')

    d.text((80, 2000), f"Motos Mes: {registrosMotosMes}", font=font_bold, fill='black')
    d.text((80, 2080), f"Total: {dineroTotalMotosMes}", font=font_bold, fill='black')

    d.text((80, 2240), f"Fijos: {registrosFijos}", font=font_bold, fill='black')
    d.text((80, 2320), f"Total: {dineroTotalFijos}", font=font_bold, fill='black')

    d.text((80, 2480), f"Registros: ", font=font_bold, fill='black')
    d.text((80, 2560), f"Total: ", font=font_bold, fill='black')

    d.text((80, 2640), f"------------------------------------------------", font=font_bold, fill='black')
    # Guardar la imagen en la ruta especificada
    img.save(ruta_guardado)
    imprimirTicket(ruta_guardado)
    print(f"Ticket Reporte Completo generado")



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
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("TicketReporteCompleto", None, "RAW"))
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
                hDC.StartDoc("TicketReporteCompleto")
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
# Ejemplo de uso
Tipo = "Todo"
FechaInicio="13-07-2024"
FechaFin = "13-07-2024"
registrosMotosHora="40"
dineroTotalMotosHora= "400000"
registrosMotosDia="30"
dineroTotalMotosDia="30000"
registrosMotosMes="20"
dineroTotalMotosMes="2000"
registrosFijos="10"
dineroTotalFijos="10000"
Fecha = "13-07-2024"
Hora = "10:17:00"
codigo = "4"


#generarTicketReporteCompleto(codigo,Tipo, FechaInicio, FechaFin,registrosMotosHora,dineroTotalMotosHora,registrosMotosDia,dineroTotalMotosDia, registrosMotosMes,dineroTotalMotosMes,registrosFijos,dineroTotalFijos ,Fecha, Hora)
