# from pywinauto import application

# ruta_ejecutable = ("C:\\Program Files (x86)\\Progress Software\\WebClient\\bin\\ChessERP®.lnk")

# app = application.Application().start(ruta_ejecutable)
import pyautogui
import time
import cv2
import numpy as np
from datetime import datetime, timedelta

pyautogui.FAILSAFE = False


fecha_actual = datetime.now()
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
#La línea 8 está solamente para hacer pruebas, la línea 6 es la correspondiente
# fecha_formateada = (fecha_actual - timedelta(days=3)).strftime("%d de %B de %Y")

months = {
    'January': 'enero',
    'February': 'febrero',
    'March': 'marzo',
    'April': 'abril',
    'May': 'mayo',
    'June': 'junio',
    'August': 'agosto',
    'September': 'septiembre',
    'October': 'octubre',
    'November': 'noviembre',
    'December': 'diciembre'

}
month = fecha_formateada.split(" de ")[1].split(" de ")[0]

if month in months:
    mes = months[month]
    fecha_real = fecha_formateada.replace(month,mes)


# Carga la imagen de la plantilla
def buscar_elemento(template_image):
    template = cv2.imread(template_image, cv2.IMREAD_GRAYSCALE)

    # Captura una captura de pantalla y conviértela a escala de grises
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)


    # Aplica Template Matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    print(result)
    # Encuentra las coordenadas donde la plantilla coincide por encima de un cierto umbral
    threshold = 0.8
    loc = np.where(result >= threshold)
    x = 0
    y = 0
    for pt in zip(*loc[::-1]):
        x, y = pt[0] + template.shape[1] / 2, pt[1] + template.shape[0] / 2
        
    return x, y


ancho, alto = pyautogui.size()
print("Dimensiones de la pantalla:")
print("Ancho:", ancho, "píxeles")
print("Alto:", alto, "píxeles")

#Abrir app ==>
resultado_x, resultado_y = buscar_elemento("template_abrir_app.png")
pyautogui.click(resultado_x, resultado_y)
pyautogui.click(resultado_x, resultado_y)
time.sleep(25)
pyautogui.press('enter')
print("Enter")
pyautogui.press('enter')
print("Enter")
time.sleep(10)


#Iniciar sesión ==>
resultado_x, resultado_y = buscar_elemento("template_usuario.png")
pyautogui.click(resultado_x, resultado_y + 15)
print("Primer click")
time.sleep(1)
pyautogui.write('sebaf')
time.sleep(1)
resultado_x, resultado_y = buscar_elemento("template_contrasena.png")
pyautogui.click(resultado_x, resultado_y + 15)
print("Segundo click")
time.sleep(1)
pyautogui.write('12345678')
time.sleep(1)
pyautogui.press('enter')
pyautogui.press('enter')
time.sleep(20)
pyautogui.press('enter')
time.sleep(5)


resultado_x, resultado_y = buscar_elemento("template_stock.png")
pyautogui.click(resultado_x, resultado_y - 5)
pyautogui.click(resultado_x, resultado_y - 5)
pyautogui.click(resultado_x, resultado_y - 5)
pyautogui.click(resultado_x, resultado_y - 5)

time.sleep(5)
resultado_x, resultado_y = buscar_elemento("template_sin_filtro.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(5)
resultado_x, resultado_y = buscar_elemento("template_bdf.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(2)
resultado_x, resultado_y = buscar_elemento("template_buscar.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(10)
resultado_x, resultado_y = buscar_elemento("template_fisico_disponible.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(2)
resultado_x, resultado_y = buscar_elemento("template_exportar.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(10)
resultado_x, resultado_y = buscar_elemento("template_file.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(2)
resultado_x, resultado_y = buscar_elemento("template_save_as.png")
pyautogui.click(resultado_x, resultado_y)
time.sleep(2)
resultado_x, resultado_y = buscar_elemento("template_this_pc.png")
pyautogui.click(resultado_x, resultado_y)
pyautogui.click(resultado_x, resultado_y)
time.sleep(2)
resultado_x, resultado_y = buscar_elemento("template_path.png")
pyautogui.click(resultado_x, resultado_y)
pyautogui.write('C:\\Users\\joaco\\Nueva carpeta\\Automatizacion PW\\archivos_xlsx_sin_limpiar')
time.sleep(1)
pyautogui.press('enter')
time.sleep(2)
resultado_x, resultado_y = buscar_elemento("template_write_name.png")
pyautogui.click(resultado_x, resultado_y)
pyautogui.press('delete')
pyautogui.write(('book_'+fecha_real).replace(" ","_"))
pyautogui.press('enter')
time.sleep(2)



