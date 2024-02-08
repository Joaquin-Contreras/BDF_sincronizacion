from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import pandas as pd
import os
import re
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

if fecha_real[0] == "0":
    fecha_real = fecha_real[1:]

#FORMATO DE FECHA A USAR:
# Ej: 8/2/2024 => 20240208

directorio = './XLSX'
nombre_archivo = re.sub(r"\s+", "_", 'mendizabal_vta_'+fecha_real+'.xlsx')
ruta_archivo = os.path.join(directorio, nombre_archivo)
print(fecha_real)


def conseguir_comprobantes_de_pago():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #Cambiar a False SOLO en testing, en deploy tiene que estar en True
        page = browser.new_page()
        context = browser.new_context()
        page.goto("http://appserver26.dyndns.org:8081/#/login")
        page.wait_for_load_state("domcontentloaded")
        try:
            page.wait_for_selector("(//*[contains(text(),'Actualizar')])[2]", timeout=50000)
            page.click("(//*[contains(text(),'Actualizar')])[2]", timeout=50000)
        except:
            print("No hay botón reinicio")
        page.wait_for_timeout(5000)
        page.fill("//input[@id='username1']", "sebaf")
        page.fill("//input[@id='pass']", "12345678")
        page.click("//button[@label='INICIAR SESIÓN']")
        page.wait_for_timeout(5000)
        
        
        #Entrar a comprobantes de pago =>
        page.click("//a[@class='menu-button']")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[2]")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[3]")
        page.wait_for_timeout(1000)
        #Entrar a comprobantes de pago <=
        #Seleccionar Fecha =>
        page.click("(//mat-datepicker-toggle)[1]")
        page.wait_for_timeout(1000)
        page.click("//button[@aria-label='"+fecha_real+"']")
        page.wait_for_timeout(2000)
        #Seleccionar Fecha <=
        #Procesar
        page.click("//button[@class='btn btn-primary ng-star-inserted']")
        page.wait_for_timeout(10000)

        #Exportar 
        with page.expect_download() as download_info:
            page.wait_for_selector("//span[@mattooltip='Exportar']")
            page.click("//span[@mattooltip='Exportar']")
            page.wait_for_timeout(3000)
            page.click("(//span[@class='mat-radio-label-content'])[2]")
            page.wait_for_timeout(1000)
            page.click("//button[@class='btn btn-md btn-primary']")
            page.wait_for_timeout(4000)
        
        descarga = download_info.value
        descarga.save_as('./CSV/mendizabal_vta_'+fecha_real+'.csv')

        browser.close()


    #TRANSFORMAR CSV A XLSX
    try:
        df_csv_old = pd.read_csv('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv', encoding='ISO-8859-1', delimiter='\t')
    except UnicodeDecodeError:
        df_csv_old = pd.read_csv('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv', encoding='cp1252', delimiter='\t')


    df = df_csv_old[['Comprobante', 'Descripcion Comprobante', 'Numero', 'Descripcion Motivo Rechazo / Devolucion', 'Vendedor', 'Descripcion Vendedor', 'Cliente', 'Subcanal', 'Codigo de Articulo', 'Descripción PROVEEDORES', 'Unidades']]
    #Convert df to XLSX



    if not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
            print(f"Directorio '{directorio}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio}': {e}")

    if os.access(directorio, os.W_OK):
        try:
            with pd.ExcelWriter('./XLSX_comprobantes_done/'+''+nombre_archivo) as writer:
                df.to_excel(writer, sheet_name="Datos", index=False)
                df.to_excel(writer, sheet_name="Verificacion", index=False)
            print(f"Archivo '{nombre_archivo}' creado correctamente en '{directorio}'.")
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio}'.")

# conseguir_comprobantes_de_pago()




with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) #Cambiar a False SOLO en testing, en deploy tiene que estar en True
    page = browser.new_page()
    context = browser.new_context()
    page.goto("http://appserver26.dyndns.org:8081/#/login")
    page.wait_for_load_state("domcontentloaded")
    try:
        page.wait_for_selector("(//*[contains(text(),'Actualizar')])[2]", timeout=50000)
        page.click("(//*[contains(text(),'Actualizar')])[2]", timeout=50000)
    except:
        print("No hay botón reinicio")
    page.wait_for_timeout(5000)
    page.fill("//input[@id='username1']", "sebaf")
    page.fill("//input[@id='pass']", "12345678")
    page.click("//button[@label='INICIAR SESIÓN']")
    page.wait_for_timeout(5000)

    page.click("//a[@class='menu-button']")
    page.wait_for_timeout(1000)
    page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[2]")
    page.wait_for_timeout(1000)
    page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[4]")
    page.wait_for_timeout(1000)


    #Exportar 
    with page.expect_download() as download_info:
        page.click("//span[@mattooltip='Exportar clientes']")
        page.wait_for_timeout(1000)
        page.click("//button[contains(text(),'Exportar')]")
        page.wait_for_timeout(1000)
        
    descarga = download_info.value
    descarga.save_as('./CSV_clientes_old/mendizabal_mc_'+fecha_real+'.csv')


    browser.close()




