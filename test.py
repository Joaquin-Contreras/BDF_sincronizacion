import pytz
import schedule
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import re
import random
import time


fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
# fecha_formateada = (fecha_actual).strftime("%d de %B de %Y")
#La línea 8 está solamente para hacer pruebas, la línea 6 es la correspondiente
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1



# Obtener la zona horaria de Argentina
zona_horaria_argentina = pytz.timezone('America/Argentina/Buenos_Aires')

# Calcular la hora local actual en Argentina
hora_actual_argentina = datetime.now(zona_horaria_argentina)

# Calcular la hora a la que queremos programar la tarea
hora_programada = hora_actual_argentina.replace(hour=21, minute=1, second=0, microsecond=0)




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
directorio_master_clientes = "./XLSX_master_clientes_done"


fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')

print(fecha_archivos)
print(fecha_real)

nombre_archivo_comprobantes = re.sub(r"\s+", "_", 'mendizabal_vta_'+fecha_archivos+'.xlsx')
nombre_archivo_master_clientes = re.sub(r"\s+", "_", 'mendizabal_mc_'+fecha_archivos+'.xlsx')


es_dia_sin_datos = False




def create_xlsx_comprobantes_de_pago():

    def asignar_tipo_documento(descripcion):
        if descripcion == 'NOTA DE CREDITO':
            return 'CR'
        elif descripcion == 'NOTA DE DEBITO':
            return 'DE'
        else:
            return 'OR'    
    
    #CREANDO SOLAPA datos ====>
    #TRANSFORMAR CSV A XLSX
    try:
        df_csv_old = pd.read_csv('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv', encoding='ISO-8859-1', delimiter='\t')
    except UnicodeDecodeError:
        df_csv_old = pd.read_csv('./CSV_comprobantes_old/mendizabal_vta_'+fecha_real+'.csv', encoding='cp1252', delimiter='\t')
    #Seleccionando las columnas que voy a necesitar
    df = df_csv_old[['Descripcion Comprobante', 'Numero', 'Descripcion Motivo Rechazo / Devolucion', 'Vendedor', 'Descripcion Vendedor', 'Cliente', 'Subcanal', 'Codigo de Articulo', 'Unidades', 'Fecha Comprobante', 'PROVEEDORES']]    # 'Comprobante'
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

    df['IdPaquete'] = valorIdPaquete
    df['IdPaquete'] = df['IdPaquete'].astype(int)

    df[['ApellidoVendedor', 'NombreVendedor']] = df['Descripcion Vendedor'].str.split(n=1, expand=True)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    # Aplicar la función a la columna 'Descripcion Comprobante' para crear la nueva columna 'TipoDocumento'
    df['TipoDocumento'] = df['Descripcion Comprobante'].apply(asignar_tipo_documento)
    df['NroComprobanteAsociado'] = np.where(df['Descripcion Comprobante'] == 'NOTA DE CREDITO', df['NroComprobante'], np.nan)
    df.drop('Descripcion Vendedor', axis=1, inplace=True)
    df.drop('Descripcion Comprobante', axis=1, inplace=True)

    df = df[['IdDistribuidor', 'IdPaquete', 'IdCliente', 'IdTipoDeCliente', 'IdVendedor', 'NombreVendedor', 
         'ApellidoVendedor', 'IdProducto', 'UnidadMedida', 'Fecha', 'TipoDocumento', 'Cantidad', 
         'NroComprobante', 'NroComprobanteAsociado', 'MotivoCR']]
    
    df = df[df['IdProducto'].apply(lambda x: x > 0)]
    df = df[(df['TipoDocumento'] != 'CR') | (df['Cantidad'] != 0)]
    df['IdTipoDeCliente'] = df['IdTipoDeCliente'].replace(9, 8)
    df['IdTipoDeCliente'] = df['IdTipoDeCliente'].replace(11, 8)
    df['PROVEEDORES'] = df_csv_old['PROVEEDORES']
    df = df[df['PROVEEDORES'].apply(lambda x: x == 1004)]
    df.drop('PROVEEDORES', axis=1, inplace=True)
    

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
            with pd.ExcelWriter('./XLSX_comprobantes_done/'+''+nombre_archivo_comprobantes) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
            print(f"Archivo '{nombre_archivo_comprobantes}' creado correctamente en '{directorio_comprobantes_de_pago}'.")
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_comprobantes}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio_comprobantes_de_pago}'.")





def get_xlsx_without_data_comprobantes_de_pago():
    df = pd.DataFrame(columns=["NroComprobante", "MotivoCR", "IdVendedor", "IdCliente",
                            "IdTipoDeCliente", "Fecha", "IdPaquete", "IdProducto",
                            "NroComprobanteAsociado", "TipoDocumento", "UnidadMedida",
                            "Unidades", "IdDistribuidor", "Apellido", "Nombre"])
    df_verificacion = pd.DataFrame(data={'IDICADOR': ['CantRegistros', 'TotalUnidades'], 'VALOR': [0, 0]})

    #Convirtiendo DF a XLSX y creando la solapa datos
    if os.access(directorio_comprobantes_de_pago, os.W_OK):
        try:
            with pd.ExcelWriter('./XLSX_comprobantes_done/'+''+nombre_archivo_comprobantes) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
                print(f"Archivo '{nombre_archivo_comprobantes}' creado correctamente en '{directorio_comprobantes_de_pago}'.")
        except Exception as e:
                print(f"Error al crear el archivo '{nombre_archivo_comprobantes}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio_comprobantes_de_pago}'.")












def conseguir_comprobantes_de_pago():



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
        toast_item_exists = False
        es_dia_sin_datos = False

        try: 
            toast_item_exists = page.inner_text('p-toastitem') is not None
        except:
            pass
            
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
        create_xlsx_comprobantes_de_pago()
    else:
        get_xlsx_without_data_comprobantes_de_pago()











def create_xlsx_master_clientes():

    equivalencias = {
    'SPM Y AUTOS. CHICO': 1, 
    'MAYORISTAS': 2, 
    'PERF. Y CASA DE ART LIMP.': 3, 
    'DROGUERIAS': 4, 
    'FERRETERIAS': 5, 
    'FARMACIA': 6, 
    'KIOSCOS Y EESS': 7, 
    'OTROS': 8, 
    'SPM Y AUTOS. MEDIANO': 21, 
    'SPM Y AUTOS. GRANDE': 22, 
    'ALMACENES': 23, 
    'SUCURSALES': 24, 
    'VACANTE': 52, 
    'DISTRIDIGITAL': 53, 
    'PROFESSIONAL': 54, 
    'CADENAS REGIONALES': 55
    }
    provincias = {
        'CAPITAL FEDERAL': 2,
        'BUENOS AIRES': 6,
        'CATAMARCA': 10,
        'CORDOBA': 14,
        'CORRIENTES': 18,
        'CHACO': 22,
        'CHUBUT': 26,
        'ENTRE RIOS': 30,
        'FORMOSA': 34,
        'JUJUY': 38,
        'LA PAMPA': 42,
        'LA RIOJA': 46,
        'MENDOZA': 50,
        'MISIONES': 54,
        'NEUQUEN': 58,
        'RIO NEGRO': 62,
        'SALTA': 66,
        'SAN JUAN': 70,
        'SAN LUIS': 74,
        'SANTA CRUZ': 78,
        'SANTA FE': 82,
        'SANTIAGO DEL ESTERO': 86,
        'TUCUMAN': 90,
        'TIERRA DEL FUEGO': 94
    }

    # Creando Solapa Datos ========>
    df_clientes_datos = pd.read_excel('./CSV_clientes_old/mendizabal_mc_'+fecha_archivos+'_1.xlsx', sheet_name="Clientes", header=1, skiprows=[2])

    df_jerarquiaMKT_datos = pd.read_excel('./CSV_clientes_old/mendizabal_mc_'+fecha_archivos+'_1.xlsx', sheet_name="Jerarquía MKT", header=1)

    df_localidades = pd.read_excel('XLSX_localidades_provincias/Localidades.xlsx', sheet_name="Localidades", header=1)

    df = pd.DataFrame()
    df['IdDistribuidor'] = ["40379573"] * len(df_clientes_datos)

    df['IdPaquete'] = valorIdPaquete

    df['IdCliente'] = df_clientes_datos['Cliente']
    df['RazonSocial'] = df_clientes_datos['Razón social']
    df['BannerText'] = ""

    df_merged_prov = pd.DataFrame()
    df_merged_prov['codigo_localidad'] = df_clientes_datos['Código Localidad']
    codigo_to_provincia = dict(zip(df_localidades['Id'], df_localidades['Provincia']))
    df_merged_prov['Provincia'] = df_merged_prov['codigo_localidad'].map(codigo_to_provincia)
    df['IdProvincia'] = pd.to_numeric(df_merged_prov['Provincia'].map(provincias), errors='coerce')

    df['Localidad'] = df_clientes_datos['Código Localidad']
    df_merged_l = pd.DataFrame()
    df_merged_l['codigo_localidad'] = df_clientes_datos['Código Localidad']
    codigo_to_localidad = dict(zip(df_localidades['Id'], df_localidades['Localidad']))
    df_merged_l['Localidad'] = df_merged_l['codigo_localidad'].map(codigo_to_localidad)
    df['Localidad'] = df['Localidad'].map(df_merged_l['Localidad'])


    df_merged_cp = pd.DataFrame()
    df_merged_cp['codigo_localidad'] = df_clientes_datos['Código Localidad']
    codigo_to_cp = dict(zip(df_localidades['Id'], df_localidades['Código Postal']))
    df_merged_cp['CodigoPostal'] = df_merged_cp['codigo_localidad'].map(codigo_to_cp)
    df['CodigoPostal'] = (df_merged_cp['CodigoPostal']).astype(int).replace(',','.')

    df['Calle'] = df_clientes_datos['Calle']
    df['Numero'] = df_clientes_datos['Altura']
    df['CUIT'] = df_clientes_datos['Identificador'].astype(str)
    df['Latitud'] = df_clientes_datos['Latitud']
    df['Longitud'] = df_clientes_datos['Longitud']

    df_merged = pd.DataFrame()
    # Agregamos la columna 'Subcanal MKT' de df1 al nuevo DataFrame
    df_merged['Subcanal MKT'] = df_clientes_datos['Subcanal MKT']
    # Creamos un diccionario para mapear los valores de 'Código' en df1 con los valores correspondientes de 'Subcanal MKT' en df2
    codigo_to_subcanal = dict(zip(df_jerarquiaMKT_datos['Código'], df_jerarquiaMKT_datos['Subcanal MKT']))
    # Mapeamos los valores de 'Código' en df1 con los valores correspondientes de 'Subcanal MKT' en df2
    df_merged['Subcanal MKT'] = df_merged['Subcanal MKT'].map(codigo_to_subcanal)
    df['IdTipoCliente'] = df_merged['Subcanal MKT'].map(equivalencias)
    

    df = df.dropna(subset=['IdTipoCliente'])
    df = df.dropna(subset=['Localidad'])
    df['IdTipoCliente'] = (df['IdTipoCliente']).astype(int)
    df = df[df['CUIT'].apply(lambda x: len(str(x)) >= 11)]
    df = df[df['RazonSocial'].apply(lambda x: '(' not in str(x) and ')' not in str(x))]
    df.reset_index(drop=True, inplace=True)
    #<======== Creando Solapa Datos 

    

    # CREANDO SOLAPA verificacion =====>
    total_registros = len(df)
    data = {'IDICADOR': ['CantRegistros']}
    df_verificacion = pd.DataFrame(data)
    df_verificacion['VALOR'] = [total_registros]
    #<===== CREANDO SOLAPA verificacion


    if not os.path.exists(directorio_master_clientes):
        try:
            os.makedirs(directorio_master_clientes)
            print(f"Directorio '{directorio_master_clientes}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_master_clientes}': {e}")


    
    if os.access(directorio_master_clientes, os.W_OK):
        try:
            with pd.ExcelWriter('./XLSX_master_clientes_done/'+''+nombre_archivo_master_clientes, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
            print(f"Archivo '{nombre_archivo_master_clientes}' creado correctamente en '{directorio_master_clientes}'.")
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_master_clientes}': {e}")
    else:
        print(f"No tienes permisos para escribir en el directorio '{directorio_master_clientes}'.")


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
            

        download = download_info.value
        download.save_as('./CSV_clientes_old/mendizabal_mc_'+fecha_archivos+'_1.xlsx')


        browser.close()

    create_xlsx_master_clientes()



# conseguir_comprobantes_de_pago()
# conseguir_clientes()


schedule.every().day.at(hora_programada.strftime("%H:%M")).do(conseguir_comprobantes_de_pago)
schedule.every().day.at(hora_programada.strftime("%H:%M")).do(conseguir_clientes)



while True:
    schedule.run_pending()
    time.sleep(1)