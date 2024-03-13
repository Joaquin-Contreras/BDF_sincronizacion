from datetime import datetime, timedelta
import pandas as pd
import uuid
from POST import inventario_bdf_post, master_clientes_bdf_post, ventas_bdf_post, fac_scj_post, inventario_scj_post
import enviar_correos

id_unico = uuid.uuid4()
fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')
hora_actual = datetime.now()
hora_formateada = hora_actual.strftime('%H-%M-%S')


fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1
json_inv = None
json_mc = None
json_vta = None

value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="

data = None
print(fecha_archivos)

def generar_archivo_respuesta_BDF():

    urls_testing = {
        "inv_bdf": 'https://dev.BDFdistribuidores.com/ws/inv',
        "mc_bdf": 'https://dev.BDFdistribuidores.com/ws/mc',
        "vta_bdf": 'https://dev.BDFdistribuidores.com/ws/vta'
    }
    urls = {        
        "inv_bdf": "https://mendizabal.BDFdistribuidores.com/ws/inv",
        "mc_bdf": "https://mendizabal.BDFdistribuidores.com/ws/mc",
        "vta_bdf": "https://mendizabal.BDFdistribuidores.com/ws/vta"
    }

    print("INVENTARIO_BDF")
    json_inv = inventario_bdf_post.inventario_bdf_post(urls_testing)
    print("MASTER_CLIENTES_BDF")
    json_mc = master_clientes_bdf_post.master_clientes_bdf_post(urls_testing)
    print("VENTAS_BDF")
    json_vta = ventas_bdf_post.ventas_bdf_post(urls_testing)

    df = pd.DataFrame()


    # Crear un diccionario con los datos que queremos asignar al DataFrame
    data = {
        'Id': id_unico,
        'Fecha': fecha_datetime,
        'Hora': hora_formateada,
        'respuesta_inv_status': json_inv.get('success', 'N/A'),
        'respuesta_inv_id': json_inv.get('id', 'N/A'),
        'respuesta_inv_detail': json_inv.get('detail', 'N/A'),  
        'respuesta_inv_message': json_inv.get('message', 'N/A'),
        'respuesta_mc_status': json_mc.get('success', 'N/A'),
        'respuesta_mc_id': json_mc.get('id', 'N/A'),
        'respuesta_mc_detail': json_mc.get('detail', 'N/A'),  
        'respuesta_mc_message': json_mc.get('message', 'N/A'),
        'respuesta_vta_status': json_vta.get('success', 'N/A'),
        'respuesta_vta_id': json_vta.get('id', 'N/A'),
        'respuesta_vta_detail': json_vta.get('detail', 'N/A'),  
        'respuesta_vta_message': json_vta.get('message', 'N/A'),
    }

    # Crear el DataFrame con una sola fila a partir del diccionario
    df = pd.DataFrame([data])

    # Nombre del archivo de Excel
    archivo_excel = './respuestas/respuesta_BDF.xlsx'

    # Crear un DataFrame de ejemplo (reemplaza esto con tus datos)
    nuevo_registro = df

    # Intenta leer el archivo existente
    try:
        df_existente = pd.read_excel(archivo_excel)
        # Agrega el nuevo registro al DataFrame existente
        df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
    except FileNotFoundError:  # Si el archivo no existe, crea uno nuevo con el registro
        df_actualizado = nuevo_registro

    # Escribe el DataFrame actualizado en el archivo de Excel
    df_actualizado.to_excel(archivo_excel, index=False)


def generar_archivo_respuesta_SCJ():

    urls_testing = {
        "fac_scj": "http://developers.dinesys2.com/ws/fac",
        "inv_scj": "http://developers.dinesys2.com/ws/inventario"
    }
    urls = {
        "fac_scj": "http://mendizabal.dinesys2.com/ws/fac",
        "inv_scj": "http://mendizabal.dinesys2.com/ws/inventario"   
    }

    print("FACTURACION_SCJ")
    json_fac = fac_scj_post.fac_scj_post(urls_testing)
    print("INVENTARIO_SCJ")
    json_inv_scj = inventario_scj_post.inventario_scj_post(urls_testing)

    # df = pd.DataFrame()


    # # Crear un diccionario con los datos que queremos asignar al DataFrame
    # data = {
    #     'Id': id_unico,
    #     'Fecha': fecha_datetime,
    #     'Hora': hora_formateada,
    #     'respuesta_fac_status': json_fac.get('success', 'N/A'),
    #     'respuesta_fac_id': json_fac.get('id', 'N/A'),
    #     'respuesta_fac_detail': json_fac.get('detail', 'N/A'),
    #     'respuesta_fac_message': json_fac.get('message', 'N/A'),
    #     'respuesta_inv_scj_status': json_inv_scj.get('success', 'N/A'),
    #     'respuesta_inv_scj_id': json_inv_scj.get('id', 'N/A'),
    #     'respuesta_inv_scj_detail': json_inv_scj.get('detail', 'N/A'),
    #     'respuesta_inv_scj_message': json_inv_scj.get('message', 'N/A'),
    # }

    # # Crear el DataFrame con una sola fila a partir del diccionario
    # df = pd.DataFrame([data])

    # # Nombre del archivo de Excel
    # archivo_excel = './respuestas/respuesta_SCJ.xlsx'

    # # Crear un DataFrame de ejemplo (reemplaza esto con tus datos)
    # nuevo_registro = df

    # # Intenta leer el archivo existente
    # try:
    #     df_existente = pd.read_excel(archivo_excel)
    #     # Agrega el nuevo registro al DataFrame existente
    #     df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
    # except FileNotFoundError:  # Si el archivo no existe, crea uno nuevo con el registro
    #     df_actualizado = nuevo_registro

    # # Escribe el DataFrame actualizado en el archivo de Excel
    # df_actualizado.to_excel(archivo_excel, index=False)   



generar_archivo_respuesta_BDF()
generar_archivo_respuesta_SCJ()

# enviar_correos.enviar_correos("joacontre0@gmail.com", data)