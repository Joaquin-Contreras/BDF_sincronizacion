from playwright.sync_api import sync_playwright
import pyautogui
import time
import cv2
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import os
import re
import time

pyautogui.FAILSAFE = False

fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
# fecha_formateada = (fecha_actual).strftime("%d de %B de %Y")
#La línea 8 está solamente para hacer pruebas, la línea 6 es la correspondiente
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1

fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')

fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')


nombre_archivo_inventario = re.sub(r"\s+", "_", 'mendizabal_inv_'+fecha_archivos+'.xlsx')

directorio = './XLSX_inventario_old'
directorio_done = './XLSX_inventario_done'

directorio_scj = './XLSX_inventario_old_scj'
directorio_done_scj = './XLSX_inventario_done_scj'


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

if not os.path.exists(directorio_scj):
    try:
        os.makedirs(directorio_scj)
        print(f"Directorio '{directorio_scj}' creado correctamente.")
    except OSError as e:
        print(f"No se pudo crear el directorio '{directorio_scj}': {e}")


def scrapear_app():
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
    time.sleep(25)
    resultado_x, resultado_y = buscar_elemento("template_ok.png")
    pyautogui.click(resultado_x, resultado_y)
    # pyautogui.press('enter')
    # pyautogui.press('enter')
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)
    resultado_x, resultado_y = buscar_elemento("template_stock.png")
    pyautogui.click(resultado_x, resultado_y - 5)
    pyautogui.click(resultado_x, resultado_y - 5)
    # pyautogui.click(resultado_x, resultado_y - 5)
    time.sleep(5)
    resultado_x, resultado_y = buscar_elemento("template_sin_filtro.png")
    pyautogui.click(resultado_x, resultado_y)
    time.sleep(6)
    resultado_x, resultado_y = buscar_elemento("template_bdf.png")
    pyautogui.click(resultado_x, resultado_y)
    time.sleep(5)
    resultado_x, resultado_y = buscar_elemento("template_buscar.png")
    pyautogui.click(resultado_x, resultado_y)
    time.sleep(10)
    # resultado_x, resultado_y = buscar_elemento("template_fisico_disponible.png")
    # pyautogui.click(resultado_x, resultado_y)
    # time.sleep(2)
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
    pyautogui.click(resultado_x - 40, resultado_y)
    pyautogui.write("C:/Users/joaco/Nueva carpeta/BDF_sincronizacion_github/BDF_sincronizacion/XLSX_inventario_old")
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    resultado_x, resultado_y = buscar_elemento("template_write_name.png")
    pyautogui.click(resultado_x, resultado_y)
    pyautogui.press('delete')
    pyautogui.write('XLSX_inventario_old'+fecha_archivos)
    pyautogui.press('enter')
    time.sleep(2)
    resultado_x, resultado_y = buscar_elemento("template_cerrar_excel.png")
    pyautogui.click(resultado_x, resultado_y)

    pyautogui.hotkey('alt', 'f4')
    time.sleep(10)
    pyautogui.press('enter')
    time.sleep(10)

    resultado_x, resultado_y = buscar_elemento("template_sin_filtro.png")
    pyautogui.click(resultado_x, resultado_y)
    time.sleep(6)
    resultado_x, resultado_y = buscar_elemento("template_scj.png")
    pyautogui.click(resultado_x, resultado_y)
    time.sleep(5)
    resultado_x, resultado_y = buscar_elemento("template_buscar.png")
    pyautogui.click(resultado_x, resultado_y)
    time.sleep(10)
    # resultado_x, resultado_y = buscar_elemento("template_fisico_disponible.png")
    # pyautogui.click(resultado_x, resultado_y)
    # time.sleep(2)
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
    pyautogui.click(resultado_x - 40, resultado_y)
    pyautogui.write("C:/Users/joaco/Nueva carpeta/BDF_sincronizacion_github/BDF_sincronizacion/XLSX_inventario_old_scj")
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    resultado_x, resultado_y = buscar_elemento("template_write_name.png")
    pyautogui.click(resultado_x, resultado_y)
    pyautogui.press('delete')
    pyautogui.write('XLSX_inventario_old_scj'+fecha_archivos)
    pyautogui.press('enter')
    time.sleep(2)
    resultado_x, resultado_y = buscar_elemento("template_cerrar_excel.png")
    pyautogui.click(resultado_x, resultado_y)



def generar_archivo_inventario():

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Cambiar a False SOLO en testing, en deploy tiene que estar en True
        page = browser.new_page()
        context = browser.new_context()
        page.goto("http://appserver26.dyndns.org:8081/#/login")
        page.wait_for_load_state("domcontentloaded")
        try:
            page.wait_for_selector(
                "(//*[contains(text(),'Actualizar')])[2]", timeout=50000
            )
            page.click("(//*[contains(text(),'Actualizar')])[2]", timeout=50000)
        except:
            print("No hay botón reinicio")
        page.wait_for_timeout(5000)
        page.fill("//input[@id='username1']", "sebaf")
        page.fill("//input[@id='pass']", "12345678")
        page.click("//button[@label='INICIAR SESIÓN']")
        page.wait_for_timeout(5000)

        try:
            page.click("//button[@class='btn btn-default']")
        except:
            pass

        page.click("//a[@class='menu-button']")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[2]")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[6]")
        page.wait_for_timeout(4000)

        #Exportar
        with page.expect_download() as download_info:        
            page.click("//span[@mattooltip='Exportar artículos']")
            page.wait_for_timeout(4000)
            page.fill("//input[@formcontrolname='buscador']", "bdf")
            page.wait_for_timeout(1500)
            page.click("//button[@class='btn btn-md btn-primary']")

        if not os.path.exists("./XLSX_inv_skus_bdf"):
            try:
                os.makedirs("./XLSX_inv_skus_bdf")
                print(f"Directorio '{"./XLSX_inv_skus_bdf"}' creado correctamente.")
            except OSError as e:
                print(f"No se pudo crear el directorio '{"./XLSX_inv_skus_bdf"}': {e}")

        download = download_info.value
        download.save_as("./XLSX_inv_skus_bdf/inv_sku_bdf" + fecha_archivos + ".xlsx")

        browser.close()



    def asignar_tipo_inventario(stock):
        if stock == 0:
            return "3"
        else:
            return "1"


    df = pd.DataFrame()

    df_inventario = pd.read_excel('./XLSX_inventario_old/XLSX_inventario_old'+fecha_archivos+'.xlsx', header=1)

    df_skus = pd.read_excel('./XLSX_inv_skus_bdf/inv_sku_bdf' + fecha_archivos + '.xlsx', header=1)

    df_skus = df_skus.drop([0])

    #CANTIDAD = (df_skus['Unidad x Bulto'] * df_inventario['Bultos']) + df_inventario['Unids']

    df['IdDistribuidor'] = [40379573] * len(df_inventario)
    df['IdPaquete'] = valorIdPaquete
    df['IdProducto'] = df_inventario['Artículo']
    df['UnidadMedida'] = "PC"
    df['Fecha'] = fecha_datetime
    df['IdTipoInventario'] = (((df_skus['Unidad x Bulto'] * df_inventario['Bultos']) + df_inventario['Unids']).fillna(0)).apply(asignar_tipo_inventario)
    df['Deposito'] = ""
    df['Cantidad'] = (df_skus['Unidad x Bulto'] * df_inventario['Bultos']) + df_inventario['Unids']
    df['Cantidad'] = df['Cantidad'].fillna(0)

    total_registros = len(df_inventario)
    suma_cantidad = df['Cantidad'].sum()
    data = {'IDICADOR': ['CantRegistros', 'TotalUnidades']}
    df_verificacion = pd.DataFrame(data)
    df_verificacion['VALOR'] = [total_registros, suma_cantidad]


    df['IdProducto'] = df['IdProducto'].replace(850882, 85088)
    df['IdProducto'] = df['IdProducto'].replace(850772, 85077)
    df['IdProducto'] = df['IdProducto'].replace(852862, 85286)
    df['IdProducto'] = df['IdProducto'].replace(880012, 88001)
    df['IdProducto'] = df['IdProducto'].replace(850612, 85061)
    df['IdProducto'] = df['IdProducto'].replace(850632, 85063)
    df['IdProducto'] = df['IdProducto'].replace(850662, 85066)


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






def generar_archivo_inventario_scj():

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Cambiar a False SOLO en testing, en deploy tiene que estar en True
        page = browser.new_page()
        context = browser.new_context()
        page.goto("http://appserver26.dyndns.org:8081/#/login")
        page.wait_for_load_state("domcontentloaded")
        try:
            page.wait_for_selector(
                "(//*[contains(text(),'Actualizar')])[2]", timeout=50000
            )
            page.click("(//*[contains(text(),'Actualizar')])[2]", timeout=50000)
        except:
            print("No hay botón reinicio")
        page.wait_for_timeout(5000)
        page.fill("//input[@id='username1']", "sebaf")
        page.fill("//input[@id='pass']", "12345678")
        page.click("//button[@label='INICIAR SESIÓN']")
        page.wait_for_timeout(5000)

        try:
            page.click("//button[@class='btn btn-default']")
        except:
            pass

        page.click("//a[@class='menu-button']")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[2]")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[6]")
        page.wait_for_timeout(4000)

        #Exportar
        with page.expect_download() as download_info:        
            page.click("//span[@mattooltip='Exportar artículos']")
            page.wait_for_timeout(4000)
            page.fill("//input[@formcontrolname='buscador']", "scj")
            page.wait_for_timeout(1500)
            page.click("//button[@class='btn btn-md btn-primary']")

        if not os.path.exists("./XLSX_inv_skus_scj"):
            try:
                os.makedirs("./XLSX_inv_skus_scj")
                print(f"Directorio '{"./XLSX_inv_skus_scj"}' creado correctamente.")
            except OSError as e:
                print(f"No se pudo crear el directorio '{"./XLSX_inv_skus_scj"}': {e}")

        download = download_info.value
        download.save_as("./XLSX_inv_skus_scj/inv_sku_scj" + fecha_archivos + ".xlsx")

        browser.close()

    
    directorio_done_scj = "./XLSX_inventario_done_scj/"
    nombre_archivo_inventario_scj = "mendizabal_inv_" + fecha_archivos + ".xlsx"

    df_old = pd.read_excel('./XLSX_inventario_old_scj/XLSX_inventario_old_scj'+fecha_archivos+'.xlsx', header=1)

    df_skus = pd.read_excel('./XLSX_inv_skus_scj/inv_sku_scj'+fecha_archivos+'.xlsx', header=1)
    df_skus = df_skus.drop([0])

    df = pd.DataFrame()

    df['IdDistribuidor'] = [15426] * len(df_old)
    df['IdPaquete'] = valorIdPaquete
    df['Fecha'] = fecha_datetime
    df['IdProducto'] = df_old['Artículo']
    df['Cantidad'] = ((df_old['Unids'] * 1) / df_skus['Unidad x Bulto']) + df_old['Bultos']
    df['Cantidad'] = (df['Cantidad'] + 0.01).astype(float)
    df['Cantidad'] = (df['Cantidad'].apply(lambda x: "{:.2f}".format(x))).astype(float)
    df['Cantidad'] = df['Cantidad'].fillna(0)
    ####SOLAPA VERIFICACIÓN =====>
    df_verificacion = pd.DataFrame()
    suma_cantidad = (df['Cantidad'].astype(float)).sum()
    df_verificacion["IDICADOR"] = ["CantRegistros", "TotalCajas"]
    df_verificacion["VALOR"] = [len(df), suma_cantidad]


    if not os.path.exists(directorio_done_scj):
        try:
            os.makedirs(directorio_done_scj)
            print(f"Directorio '{directorio_done_scj}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_done_scj}': {e}")


    if os.access(directorio_done_scj, os.W_OK):
        try:
            with pd.ExcelWriter(directorio_done_scj+'/'+nombre_archivo_inventario_scj) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
            print(f"Archivo '{nombre_archivo_inventario_scj}' creado correctamente en '{directorio_done_scj}'.")
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_inventario_scj}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio_done_scj}'.") 






# scrapear_app()
# generar_archivo_inventario()
generar_archivo_inventario_scj()

