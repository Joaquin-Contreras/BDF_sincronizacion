from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os
import create_xlsx_master_clientes
import create_xlsx_comprobantes_de_pago
import generar_archivo_facturacion_scj
import get_xlsx_without_data_comprobantes_de_pago
import generar_archivo_fac_sin_datos
import generar_archivo_articulos
import generar_archivo_clientes_dinesys
import enviar_correos
import subprocess
import time

dias_a_restar = 1


fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
# fecha_formateada = (fecha_actual).strftime("%d de %B de %Y")
# La línea 8 está solamente para hacer pruebas, la línea 6 es la correspondiente
fecha_formateada = (fecha_actual - timedelta(days=dias_a_restar)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1



months = {
    "January": "enero",
    "February": "febrero",
    "March": "marzo",
    "April": "abril",
    "May": "mayo",
    "June": "junio",
    "August": "agosto",
    "September": "septiembre",
    "October": "octubre",
    "November": "noviembre",
    "December": "diciembre",
}
month = fecha_formateada.split(" de ")[1].split(" de ")[0]

if month in months:
    mes = months[month]
    fecha_real = fecha_formateada.replace(month, mes)

if fecha_real[0] == "0":
    fecha_real = fecha_real[1:]

dia_de_la_semana = (fecha_actual - timedelta(days=dias_a_restar)).strftime("%A")


fecha_archivos_menos_un_dia_str = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=dias_a_restar)
fecha_archivos = fecha_archivos_menos_un_dia.strftime("%Y%m%d")

print(fecha_archivos)
print(fecha_real)

def conseguir_comprobantes_de_pago_y_fac_bdf_scj():
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

        # Entrar a comprobantes de pago =>
        page.click("//a[@class='menu-button']")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[2]")
        page.wait_for_timeout(1000)
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[3]")
        page.wait_for_timeout(1000)
        # Entrar a comprobantes de pago <=
        # Seleccionar Fecha =>
        page.click("(//mat-datepicker-toggle)[1]")
        page.wait_for_timeout(3000)
        page.click("//button[@aria-label='" + fecha_real + "']")
        page.wait_for_timeout(2000)
        # Seleccionar Fecha <=

        page.click("//button[@class='btn btn-primary ng-star-inserted']")
        toast_item_exists = False
        es_dia_sin_datos = False

        try:
            toast_item_exists = page.inner_text("p-toastitem") is not None
        except:
            pass

        page.wait_for_timeout(10000)

        if dia_de_la_semana == "Sunday":
            es_dia_sin_datos = True
            print("No hay datos para el dia" + " " + fecha_real)

        if not toast_item_exists:
            # Exportar
            with page.expect_download() as download_info:
                page.wait_for_selector("//span[@mattooltip='Exportar']")
                page.click("//span[@mattooltip='Exportar']")
                page.wait_for_timeout(3000)
                page.click("(//span[@class='mat-radio-label-content'])[2]")
                page.wait_for_timeout(1000)
                page.click("//button[@class='btn btn-md btn-primary']")
                page.wait_for_timeout(4000)

                if not os.path.exists("./CSV_comprobantes_old"):
                    try:
                        os.makedirs("./CSV_comprobantes_old")
                        print("Directorio /CSV_comprobantes_old creado exitosamente")
                    except:
                        print("No se pudo crear el directorio /CSV_comprobantes_old")

                descarga = download_info.value
                descarga.save_as(
                    "./CSV_comprobantes_old/mendizabal_vta_" + fecha_real + ".csv"
                )
        else:
            es_dia_sin_datos = True
            print("No hay datos para el dia" + " " + fecha_real)

        browser.close()
    if not es_dia_sin_datos:
        create_xlsx_comprobantes_de_pago.create_xlsx_comprobantes_de_pago(dias_a_restar=dias_a_restar)
        generar_archivo_facturacion_scj.generar_archivo_facturacion_scj(dias_a_restar=dias_a_restar)
    else:
        get_xlsx_without_data_comprobantes_de_pago.get_xlsx_without_data_comprobantes_de_pago(dias_a_restar=dias_a_restar)
        generar_archivo_fac_sin_datos.generar_archivo_fac_sin_datos(dias_a_restar=dias_a_restar)



def conseguir_clientes():
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
        page.click("(//a[contains(@class,'p-ripple p-element ng-tns-c5')])[4]")
        page.wait_for_timeout(1000)

        # Exportar
        with page.expect_download() as download_info:
            page.click("//span[@mattooltip='Exportar clientes']")
            page.wait_for_timeout(1000)
            page.click("//button[contains(text(),'Exportar')]")
            page.wait_for_timeout(1000)

        download = download_info.value
        download.save_as(
            "./CSV_clientes_old/mendizabal_mc_" + fecha_archivos + "_1.xlsx"
        )

        browser.close()

    create_xlsx_master_clientes.create_xlsx_master_clientes()
    # generar_archivo_clientes_dinesys.generar_archivo_clientes_dinesys()

def conseguir_inv_dinesys():
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
            page.click("//div[contains(text(),'SCJ')]")
            page.click("//button[@class='btn btn-md btn-primary']")
        
        download = download_info.value
        download.save_as("./XLSX_inv_dinesys_old/inv_dinesys_old" + fecha_archivos + ".xlsx")

        browser.close()

        generar_archivo_articulos.generar_archivo_articulos()


conseguir_comprobantes_de_pago_y_fac_bdf_scj()
conseguir_clientes()
# conseguir_inv_dinesys()
        
# create_xlsx_master_clientes.create_xlsx_master_clientes()
# create_xlsx_comprobantes_de_pago.create_xlsx_comprobantes_de_pago(dias_a_restar=dias_a_restar)
# generar_archivo_facturacion_scj.generar_archivo_facturacion_scj(dias_a_restar=dias_a_restar)
# get_xlsx_without_data_comprobantes_de_pago.get_xlsx_without_data_comprobantes_de_pago(dias_a_restar)
# generar_archivo_fac_sin_datos.generar_archivo_fac_sin_datos(dias_a_restar)
# generar_archivo_clientes_dinesys.generar_archivo_clientes_dinesys()
# create_xlsx_master_clientes.create_xlsx_master_clientes()

enviar_correos.enviar_correos("joacontre0@gmail.com", "MAIN.PY")
enviar_correos.enviar_correos("sebaf@jjmendizabal.com.ar", "MAIN.PY")
        
time.sleep(5)
script_path = "C:/Users/SebastianFuhr/Desktop/Dashboard_sincro/actualizar_repo.sh"
subprocess.run(["bash", script_path], shell=True)