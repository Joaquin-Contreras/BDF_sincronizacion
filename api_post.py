import requests
from datetime import datetime, timedelta
import json
import os
import pandas as pd

fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')



fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1

value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="


# url_inventario = 'https://dev.BDFdistribuidores.com/ws/inv'
url_inventario = "https://mendizabal.BDFdistribuidores.com/ws/inv"

directorio_inventario = "./XLSX_inventario_done/"

nombre_archivo_inventario = 'mendizabal_inv_'+fecha_archivos+'.xlsx'

archivo_inventario = directorio_inventario+nombre_archivo_inventario
json_inv = None
json_mc = None
json_vta = None

print(archivo_inventario)
with open(archivo_inventario, 'rb') as archivo:
    # Configurar los datos del archivo
    archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    datos = {'parametro_adicional': 'valor_adicional'}

    # Definir el encabezado de autorización
    encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

    # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
    respuesta = requests.post(url_inventario, files=archivos, data=datos, headers=encabezado_autorizacion)

    json_inv = json.loads(respuesta.text)
    print(respuesta.text)




# url_mc = "https://dev.BDFdistribuidores.com/ws/mc"
url_mc = "https://mendizabal.BDFdistribuidores.com/ws/mc"

directorio_mc = "./XLSX_master_clientes_done/"

nombre_archivo_inventario = 'mendizabal_mc_'+fecha_archivos+'.xlsx'

archivo_inventario = directorio_mc+nombre_archivo_inventario

print(archivo_inventario)
with open(archivo_inventario, 'rb') as archivo:
    # Configurar los datos del archivo
    # archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.ms-excel')}

    # Definir el encabezado de autorización
    encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

    # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
    respuesta = requests.post(url_mc, files=archivos, headers=encabezado_autorizacion)
    json_mc = json.loads(respuesta.text)
    print(respuesta.text)




# url_vta = "https://dev.BDFdistribuidores.com/ws/vta"
url_vta = "https://mendizabal.BDFdistribuidores.com/ws/vta"

directorio_mc = "./XLSX_comprobantes_done/"

nombre_archivo_inventario = 'mendizabal_vta_'+fecha_archivos+'.xlsx'

archivo_inventario = directorio_mc+nombre_archivo_inventario

print(archivo_inventario)
with open(archivo_inventario, 'rb') as archivo:
    # Configurar los datos del archivo
    archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

    # Definir el encabezado de autorización
    encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

    # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
    respuesta = requests.post(url_vta, files=archivos, headers=encabezado_autorizacion)
    json_vta = json.loads(respuesta.text)
    print(respuesta.text)



directorio = "./respuestas/"

df = pd.DataFrame()


# Crear un diccionario con los datos que queremos asignar al DataFrame
data = {
    'Id': valorIdPaquete,
    'Fecha': fecha_datetime,
    'respuesta_inv_status': json_inv.get('success', 'N/A'),
    'respuesta_inv_id': json_inv.get('id', 'N/A'),
    'respuesta_inv_detail': json_inv.get('detail', 'N/A'),  # Aquí suponemos que hay una clave 'detail' en el JSON
    'respuesta_inv_message': json_inv.get('message', 'N/A'),
    'respuesta_mc_status': json_mc.get('success', 'N/A'),
    'respuesta_mc_id': json_mc.get('id', 'N/A'),
    'respuesta_mc_detail': json_mc.get('detail', 'N/A'),  # Aquí suponemos que hay una clave 'detail' en el JSON
    'respuesta_mc_message': json_mc.get('message', 'N/A'),
    'respuesta_vta_status': json_vta.get('success', 'N/A'),
    'respuesta_vta_id': json_vta.get('id', 'N/A'),
    'respuesta_vta_detail': json_vta.get('detail', 'N/A'),  # Aquí suponemos que hay una clave 'detail' en el JSON
    'respuesta_vta_message': json_vta.get('message', 'N/A'),
}

# Crear el DataFrame con una sola fila a partir del diccionario
df = pd.DataFrame([data])


if not os.path.exists(directorio):
    try:
        os.makedirs(directorio)
        print(f"Directorio '{directorio}' creado correctamente.")
    except OSError as e:
        print(f"No se pudo crear el directorio '{directorio}': {e}")


if os.access(directorio, os.W_OK):
    try:
        with pd.ExcelWriter(directorio+'/respuesta.xlsx') as writer:
            df.to_excel(writer, sheet_name="respuestas", index=False)
        print(f"Archivo de respuestas creado correctamente en '{directorio}'.")
    except Exception as e:
        print(f"Error al crear el archivo de respuestas: {e}")
else:
    print(f"No tienes permisos para escribir en el directorio '{directorio}'.") 
