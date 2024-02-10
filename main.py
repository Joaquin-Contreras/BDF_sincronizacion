from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import re
fecha_actual = datetime.now()
# fecha_formateada = (fecha_actual).strftime("%d de %B de %Y")
#La línea 8 está solamente para hacer pruebas, la línea 6 es la correspondiente
fecha_formateada = (fecha_actual - timedelta(days=5)).strftime("%d de %B de %Y")

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

directorio_comprobantes_de_pago = './XLSX_comprobantes_done'
fecha_archivos = datetime.now().strftime('%Y%m%d')
nombre_archivo = re.sub(r"\s+", "_", 'mendizabal_vta_'+fecha_archivos+'.xlsx')
ruta_archivo = os.path.join(directorio_comprobantes_de_pago, nombre_archivo)
print(fecha_archivos)


es_dia_sin_datos = False




def create_xlsx():
    def asignar_tipo_documento(descripcion):
        if descripcion == 'NOTA DE CREDITO':
            return 'CR'
        elif descripcion == 'NOTA DE DEBITO':
            return 'DR'
        else:
            return 'OR'    
    
    #CREANDO SOLAPA datos ====>
    #TRANSFORMAR CSV A XLSX
    try:
        df_csv_old = pd.read_csv('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv', encoding='ISO-8859-1', delimiter='\t')
    except UnicodeDecodeError:
        df_csv_old = pd.read_csv('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv', encoding='cp1252', delimiter='\t')

    #Seleccionando las columnas que voy a necesitar
    df = df_csv_old[['Descripcion Comprobante', 'Numero', 'Descripcion Motivo Rechazo / Devolucion', 'Vendedor', 'Descripcion Vendedor', 'Cliente', 'Subcanal', 'Codigo de Articulo', 'Unidades', 'Fecha Comprobante']]    # 'Comprobante'
    # 'Descripción PROVEEDORES'
    #Renombrando columnas
    df.rename(columns={
            "Cliente": "IdCliente",
            "Subcanal": "IdTipoDeCliente",
            "Vendedor": "IdVendedor",
            "Fecha Comprobante": "Fecha",
            "Unidades": "Cantidad",
            "Numero": "NroComprobante",
            "Descripcion Motivo Rechazo / Devolucion": "MotivoCR",
            "Codigo de Articulo": "IdProducto",
            }, inplace=True)
        
        #Agregando columnas necesarias
    df["IdDistribuidor"] = "40379573"
    df["UnidadMedida"] = "PC"
    df['IdPaquete'] = range(1, len(df) + 1)
    df[['Apellido', 'Nombre']] = df['Descripcion Vendedor'].str.split(n=1, expand=True)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y').dt.strftime('%Y%m%d')

    # Aplicar la función a la columna 'Descripcion Comprobante' para crear la nueva columna 'TipoDocumento'
    df['TipoDocumento'] = df['Descripcion Comprobante'].apply(asignar_tipo_documento)
    df['NroComprobanteAsociado'] = np.where(df['Descripcion Comprobante'] == 'NOTA DE CREDITO', df['NroComprobante'], np.nan)
    df.drop('Descripcion Vendedor', axis=1, inplace=True)
    df.drop('Descripcion Comprobante', axis=1, inplace=True)




    if not os.path.exists(directorio_comprobantes_de_pago):
        try:
            os.makedirs(directorio_comprobantes_de_pago)
            print(f"Directorio '{directorio_comprobantes_de_pago}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_comprobantes_de_pago}': {e}")




    #<=====     CREANDO SOLAPA datos
    # CREANDO SOLAPA verificacion =====>
    total_registros = len(df)
    suma_cantidad = df['Cantidad'].sum()
    data = {'IDICADOR': ['CantRegistros', 'TotalUnidades']}
    df_verificacion = pd.DataFrame(data)
    df_verificacion['VALOR'] = [total_registros, suma_cantidad]
    #<===== CREANDO SOLAPA verificacion


    #Convirtiendo DF a XLSX y creando la solapa datos
    if os.access(directorio_comprobantes_de_pago, os.W_OK):
        try:
            with pd.ExcelWriter('./XLSX_comprobantes_done/'+''+nombre_archivo) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="Verificacion", index=False)
            print(f"Archivo '{nombre_archivo}' creado correctamente en '{directorio_comprobantes_de_pago}'.")
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio_comprobantes_de_pago}'.")





def get_xlsx_without_data():
    df = pd.DataFrame(columns=["NroComprobante", "MotivoCR", "IdVendedor", "IdCliente",
                            "IdTipoDeCliente", "Fecha", "IdPaquete", "IdProducto",
                            "NroComprobanteAsociado", "TipoDocumento", "UnidadMedida",
                            "Unidades", "IdDistribuidor", "Apellido", "Nombre"])
    df_verificacion = pd.DataFrame(data={'IDICADOR': ['CantRegistros', 'TotalUnidades'], 'VALOR': [0, 0]})

    #Convirtiendo DF a XLSX y creando la solapa datos
    if os.access(directorio_comprobantes_de_pago, os.W_OK):
        try:
            with pd.ExcelWriter('./XLSX_comprobantes_done/'+''+nombre_archivo) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="Verificacion", index=False)
                print(f"Archivo '{nombre_archivo}' creado correctamente en '{directorio_comprobantes_de_pago}'.")
        except Exception as e:
                print(f"Error al crear el archivo '{nombre_archivo}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio_comprobantes_de_pago}'.")












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

        page.click("//button[@class='btn btn-primary ng-star-inserted']")
        toast_item_exists = page.inner_text('p-toastitem') is not None

        page.wait_for_timeout(10000)

        if not toast_item_exists:
            #Exportar 
            with page.expect_download() as download_info:
                page.wait_for_selector("//span[@mattooltip='Exportar']")
                page.click("//span[@mattooltip='Exportar']")
                page.wait_for_timeout(3000)
                page.click("(//span[@class='mat-radio-label-content'])[2]")
                page.wait_for_timeout(1000)
                page.click("//button[@class='btn btn-md btn-primary']")
                page.wait_for_timeout(4000)

                if not os.path.exists('./CSV_comprobantes_old'):
                    try:
                        os.makedirs('./CSV_comprobantes_old')
                        print("Directorio /CSV_comprobantes_old creado exitosamente")
                    except:
                        print("No se pudo crear el directorio /CSV_comprobantes_old")

                descarga = download_info.value
                descarga.save_as('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv')
        else:
            es_dia_sin_datos = True
            print("No hay datos para el dia"+ " " + fecha_real)

        browser.close()

    if not es_dia_sin_datos:
        create_xlsx()
    else:
        get_xlsx_without_data()
conseguir_comprobantes_de_pago()







def conseguir_clientes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #Cambiar a False SOLO en testing, en deploy tiene que estar en True
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
# conseguir_clientes()
