from datetime import datetime, timedelta
import pandas as pd
import uuid
from POST import inventario_bdf_post, master_clientes_bdf_post, ventas_bdf_post
import os
import enviar_correos
import subir_archivos_a_pagina
import subprocess
import time

dias_a_restar = 1 # DESDE ACÁ SE CAMBIA LA FECHA DE LOS ARCHIVOS A ENVIAR

id_unico = uuid.uuid4()
fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=dias_a_restar)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')
hora_actual = datetime.now()
hora_formateada = hora_actual.strftime('%H-%M-%S')




fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
fecha_formateada = (fecha_actual - timedelta(days=dias_a_restar)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1
json_inv = None
json_mc = None
json_vta = None

# value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="

data = None
print(fecha_archivos)

def generar_archivo_respuesta_BDF():


    ##################DESCOMENTAR LO DE ABAJO EN TEST
    # print("USANDO URL'S DE PRUEBA")
    # is_test = True
    # urls = {
    #      "inv_bdf": 'https://dev.BDFdistribuidores.com/ws/inv',
    #      "mc_bdf": 'https://dev.BDFdistribuidores.com/ws/mc',
    #      "vta_bdf": 'https://dev.BDFdistribuidores.com/ws/vta'
    # }
    ##################

    #################DESCOMENTAR LO DE ABAJO EN PROD
    print("USANDO URL'S DE PROD")
    is_test = False
    urls = {        
       "inv_bdf": "https://mendizabal.BDFdistribuidores.com/ws/inv",
      "mc_bdf": "https://mendizabal.BDFdistribuidores.com/ws/mc",
     "vta_bdf": "https://mendizabal.BDFdistribuidores.com/ws/vta"
    }
    ##################
    
    # Diccionario para almacenar los nombres de archivo por función
    df_archivos_reenviar = pd.read_excel('reenvios/reenvios_BDF.xlsx')
    archivos_a_reenviar = {'INVENTARIO_BDF': [], 'MASTER_CLIENTES_BDF': [], 'VENTAS_BDF': []}

    # Iterar sobre las filas del DataFrame
    for _, row in df_archivos_reenviar.iterrows():
        nombre_archivo = row['nombre_archivo']
        
        # Verificar si el archivo existe
        if os.path.exists(f'reenvios/reenvios_BDF.xlsx'):
            # Determinar la función basada en el nombre del archivo
            if 'inv' in nombre_archivo:
                pass
                # archivos_a_reenviar['INVENTARIO_BDF'].append(nombre_archivo)
            elif 'mc' in nombre_archivo:
                archivos_a_reenviar['MASTER_CLIENTES_BDF'].append(nombre_archivo)
            elif 'vta' in nombre_archivo:
                archivos_a_reenviar['VENTAS_BDF'].append(nombre_archivo)

    print("#################################")
    json_inv = inventario_bdf_post.inventario_bdf_post(urls, archivos_a_reenviar['INVENTARIO_BDF'], dias_a_restar)
    print("#################################")
    json_mc = master_clientes_bdf_post.master_clientes_bdf_post(urls, archivos_a_reenviar['MASTER_CLIENTES_BDF'], dias_a_restar)
    print("#################################")
    json_vta = ventas_bdf_post.ventas_bdf_post(urls, archivos_a_reenviar['VENTAS_BDF'], dias_a_restar)

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
        'is_test': is_test
    }

    # Crear el DataFrame con una sola fila a partir del diccionario
    df = pd.DataFrame([data])

    # Nombre del archivo de Excel
    archivo_excel = './respuestas/respuesta_BDF.xlsx'

    # Intenta leer el archivo existente
    try:
        df_existente = pd.read_excel(archivo_excel)
        # Filtrar los registros existentes para el día actual y para los que no son de prueba
        filtro_fecha = df_existente['Fecha'] == fecha_datetime
        filtro_test = df_existente['is_test'] == False
        registros_existente_hoy = df_existente[filtro_fecha & filtro_test]

        # Si hay registros existentes para hoy y no son de prueba
        if not registros_existente_hoy.empty:
            # Actualizar el registro existente con el nuevo dato
            df_actualizado = pd.concat([df_existente[~(filtro_fecha & filtro_test)], df], ignore_index=True)
        else:
            # Agrega el nuevo registro al DataFrame existente
            df_actualizado = pd.concat([df_existente, df], ignore_index=True)

    except FileNotFoundError:  # Si el archivo no existe, crea uno nuevo con el registro
        df_actualizado = df

    # Escribe el DataFrame actualizado en el archivo de Excel
    df_actualizado.to_excel(archivo_excel, index=False)
    
    ruta_archivo = ruta_archivo=(archivo_excel)
    nombre_carpeta = "respuestas"
    subir_archivos_a_pagina.subir_archivos_a_pagina(ruta_archivo=ruta_archivo, nombre_carpeta=nombre_carpeta)

    time.sleep(5)

    script_path = "C:/Users/SebastianFuhr/Desktop/Dashboard_sincro/actualizar_repo.sh"
    subprocess.run(["bash", script_path], shell=True)

generar_archivo_respuesta_BDF()
enviar_correos.enviar_correos("joacontre0@gmail.com", "api_post_bdf.py")
enviar_correos.enviar_correos("sebaf@jjmendizabal.com.ar", "api_post_bdf.py")