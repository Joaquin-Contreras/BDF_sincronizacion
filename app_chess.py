# from pywinauto import application

# ruta_ejecutable = ("C:\\Program Files (x86)\\Progress Software\\WebClient\\bin\\ChessERP®.lnk")

# app = application.Application().start(ruta_ejecutable)
import pyautogui
import time
import cv2
import numpy as np
from datetime import date, datetime, timedelta
import pandas as pd
import os
import re
import random
import time

pyautogui.FAILSAFE = False


fecha_formateada = datetime.now().strftime("%Y-%m-%d")
fecha_archivos = datetime.now().strftime('%Y%m%d')
nombre_archivo_inventario = re.sub(r"\s+", "_", 'mendizabal_inv_'+fecha_archivos+'.xlsx')

directorio = './XLSX_inventario_old'
directorio_done = './XLSX_inventario_done'


def generar_id_unico():
    # Obtener el tiempo actual en milisegundos
    tiempo_actual = int(time.time() * 1000)
    # Generar un número aleatorio de 6 dígitos
    numero_aleatorio = random.randint(100000, 999999)
    # Combinar el tiempo actual y el número aleatorio para formar el ID único
    id_unico = int(f"{tiempo_actual}{numero_aleatorio}")
    return id_unico

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

print(fecha_formateada)



if not os.path.exists(directorio):
    try:
        os.makedirs(directorio)
        print(f"Directorio '{directorio}' creado correctamente.")
    except OSError as e:
        print(f"No se pudo crear el directorio '{directorio}': {e}")

# ancho, alto = pyautogui.size()
# print("Dimensiones de la pantalla:")
# print("Ancho:", ancho, "píxeles")
# print("Alto:", alto, "píxeles")

# #Abrir app ==>
# resultado_x, resultado_y = buscar_elemento("template_abrir_app.png")
# pyautogui.click(resultado_x, resultado_y)
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(25)
# pyautogui.press('enter')
# print("Enter")
# pyautogui.press('enter')
# print("Enter")
# time.sleep(10)


# #Iniciar sesión ==>
# resultado_x, resultado_y = buscar_elemento("template_usuario.png")
# pyautogui.click(resultado_x, resultado_y + 15)
# print("Primer click")
# time.sleep(1)
# pyautogui.write('sebaf')
# time.sleep(1)
# resultado_x, resultado_y = buscar_elemento("template_contrasena.png")
# pyautogui.click(resultado_x, resultado_y + 15)
# print("Segundo click")
# time.sleep(1)
# pyautogui.write('12345678')
# time.sleep(1)
# pyautogui.press('enter')
# pyautogui.press('enter')
# time.sleep(25)
# pyautogui.press('enter')
# pyautogui.press('enter')
# time.sleep(5)
# pyautogui.press('enter')
# time.sleep(5)
# resultado_x, resultado_y = buscar_elemento("template_stock.png")
# pyautogui.click(resultado_x, resultado_y - 5)
# pyautogui.click(resultado_x, resultado_y - 5)
# pyautogui.click(resultado_x, resultado_y - 5)
# pyautogui.click(resultado_x, resultado_y - 5)

# time.sleep(5)
# resultado_x, resultado_y = buscar_elemento("template_sin_filtro.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(5)
# resultado_x, resultado_y = buscar_elemento("template_bdf.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_buscar.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(10)
# resultado_x, resultado_y = buscar_elemento("template_fisico_disponible.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_exportar.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(10)
# resultado_x, resultado_y = buscar_elemento("template_file.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_save_as.png")
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_this_pc.png")
# pyautogui.click(resultado_x, resultado_y)
# pyautogui.click(resultado_x, resultado_y)
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_path.png")
# pyautogui.click(resultado_x - 30, resultado_y)
# pyautogui.write("C:/Users/joaco/Nueva carpeta/BDF_sincronizacion_github/BDF_sincronizacion/XLXS_inventario_old")
# time.sleep(1)
# pyautogui.press('enter')
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_write_name.png")
# pyautogui.click(resultado_x, resultado_y)
# pyautogui.press('delete')
# pyautogui.write('XLSX_inventario_old'+fecha_archivos)
# pyautogui.press('enter')
# time.sleep(2)
# resultado_x, resultado_y = buscar_elemento("template_cerrar_excel.png")
# pyautogui.click(resultado_x, resultado_y)



df = pd.DataFrame()

df_inventario = pd.read_excel('./XLSX_inventario_old/XLSX_inventario_old'+fecha_archivos+'.xlsx')

df['IdDistribuidor'] = ["40379573"] * len(df_inventario)
df['IdPaquete'] = generar_id_unico()
df['IdProducto'] = df_inventario['Artículo']
df['UnidadMedida'] = "PC"
df['Fecha'] = fecha_formateada
df['Cantidad'] = df_inventario['Stock disponible']



total_registros = len(df_inventario)
suma_cantidad = df_inventario['Stock disponible'].sum()
data = {'IDICADOR': ['CantRegistros', 'TotalUnidades']}
df_verificacion = pd.DataFrame(data)
df_verificacion['VALOR'] = [total_registros, suma_cantidad]




if not os.path.exists(directorio_done):
    try:
        os.makedirs(directorio_done)
        print(f"Directorio '{directorio_done}' creado correctamente.")
    except OSError as e:
        print(f"No se pudo crear el directorio '{directorio_done}': {e}")

if os.access(directorio_done, os.W_OK):
    try:
        with pd.ExcelWriter(directorio_done+'/'+nombre_archivo_inventario) as writer:
            df.to_excel(writer, sheet_name="datos", index=False)
            df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
        print(f"Archivo '{nombre_archivo_inventario}' creado correctamente en '{directorio_done}'.")
    except Exception as e:
        print(f"Error al crear el archivo '{nombre_archivo_inventario}': {e}")
else:
    print(f"No tienes permisos para escribir en el directorio '{directorio_done}'.") 


#CAMPOS:
# IdTipoInventario => ########
# Deposito => ##################



# IdDistribuidor => ["40379573"] * len(df) 
# IdPaquete => AUTO_INCREMENT
# IdProducto => Columna: Artículo
# UnidadMedida => "PC"
# Fecha => YYYY-MM-DD
# Cantidad => Columna: Stock disponible