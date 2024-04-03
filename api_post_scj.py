from datetime import datetime, timedelta
import pandas as pd
import uuid
from POST import fac_scj_post, inventario_scj_post
import os
import enviar_correos
import subir_archivos_a_pagina
import subprocess
import time

dias_a_restar = 1

id_unico = uuid.uuid4()
fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=dias_a_restar) #Si se necesita, cambiar a 2 para enviar otro día
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')
hora_actual = datetime.now()
hora_formateada = hora_actual.strftime('%H-%M-%S')


fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
fecha_formateada = (fecha_actual - timedelta(days=dias_a_restar)).strftime("%d de %B de %Y") #Acá también :3
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1
json_inv = None
json_mc = None
json_vta = None

value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="

data = None
print(fecha_archivos)



def generar_archivo_respuesta_SCJ():

    ##################DESCOMENTAR LO DE ABAJO EN TEST
    # print("USANDO URL'S DE PRUEBA")
    # is_test = True
    # urls = {
    #       "fac_scj": "http://developers.dinesys2.com/ws/fac",
    #       "inv_scj": "http://developers.dinesys2.com/ws/inventario"
    # }
    ##################

    #################DESCOMENTAR LO DE ABAJO EN PROD
    print("USANDO URL'S DE PROD")
    is_test = False
    urls = {
           "fac_scj": "http://mendizabal.dinesys2.com/ws/fac",
           "inv_scj": "http://mendizabal.dinesys2.com/ws/inventario"   
    }
    ##################


    # Diccionario para almacenar los nombres de archivo por función
    df_archivos_reenviar = pd.read_excel('reenvios/reenvios_SCJ.xlsx')
    archivos_a_reenviar = {'INVENTARIO_SCJ': [], 'FACTURACION_SCJ': []}

    # Iterar sobre las filas del DataFrame
    for _, row in df_archivos_reenviar.iterrows():
        nombre_archivo = row['nombre_archivo']
        
        # Verificar si el archivo existe
        if os.path.exists(f'reenvios/reenvios_SCJ.xlsx'):
            # Determinar la función basada en el nombre del archivo
            if 'fac' in nombre_archivo:
                archivos_a_reenviar['FACTURACION_SCJ'].append(nombre_archivo)
            elif 'inv' in nombre_archivo:
                archivos_a_reenviar['INVENTARIO_SCJ'].append(nombre_archivo)



    print("#################################")
    print("FACTURACION_SCJ")
    json_fac = fac_scj_post.fac_scj_post(urls, archivos_a_reenviar['FACTURACION_SCJ'], dias_a_restar)
    print("#################################")
    print("INVENTARIO_SCJ")
    json_inv_scj = inventario_scj_post.inventario_scj_post(urls, archivos_a_reenviar['INVENTARIO_SCJ'], dias_a_restar)

    df = pd.DataFrame()


    # Crear un diccionario con los datos que queremos asignar al DataFrame
    data = {
        'Id': id_unico,
        'Fecha': fecha_datetime,
        'Hora': hora_formateada,
        'respuesta_fac_status': json_fac.get('success', 'N/A'),
        'respuesta_fac_id': json_fac.get('id', 'N/A'),
        'respuesta_fac_detail': json_fac.get('detail', 'N/A'),
        'respuesta_fac_message': json_fac.get('message', 'N/A'),
        'respuesta_inv_scj_status': json_inv_scj.get('success', 'N/A'),
        'respuesta_inv_scj_id': json_inv_scj.get('id', 'N/A'),
        'respuesta_inv_scj_detail': json_inv_scj.get('detail', 'N/A'),
        'respuesta_inv_scj_message': json_inv_scj.get('message', 'N/A'),
        'is_test': is_test
    }

    # Crear el DataFrame con una sola fila a partir del diccionario
    df = pd.DataFrame([data])
    df['respuesta_fac_status'] = df['respuesta_fac_status'].apply(lambda x: True if x == 1 else False)

    # Nombre del archivo de Excel
    archivo_excel = './respuestas/respuesta_SCJ.xlsx'

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

    ruta_archivo = ruta_archivo=(archivo_excel)
    nombre_carpeta = "respuestas"
    subir_archivos_a_pagina.subir_archivos_a_pagina(ruta_archivo=ruta_archivo, nombre_carpeta=nombre_carpeta)
    
    time.sleep(5)

    script_path = "C:/Users/SebastianFuhr/Desktop/Dashboard_sincro/actualizar_repo.sh"
    subprocess.run(["bash", script_path], shell=True)



generar_archivo_respuesta_SCJ()

enviar_correos.enviar_correos("joacontre0@gmail.com", "api_post_scj.py")
enviar_correos.enviar_correos("sebaf@jjmendizabal.com.ar", "api_post_scj.py")