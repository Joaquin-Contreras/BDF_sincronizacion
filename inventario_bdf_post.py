import requests
from datetime import datetime, timedelta
import json
import pandas as pd
import uuid


id_unico = uuid.uuid4()
fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')
hora_actual = datetime.now()
hora_formateada = hora_actual.strftime('%H-%M-%S')




value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="

def inventario_bdf_post():
    try:
        url_inventario = 'https://dev.BDFdistribuidores.com/ws/inv'
        # url_inventario = "https://mendizabal.BDFdistribuidores.com/ws/inv"

        directorio_inventario = "./XLSX_inventario_done/"

        nombre_archivo_inventario = 'mendizabal_inv_'+fecha_archivos+'.xlsx'

        archivo_inventario = directorio_inventario+nombre_archivo_inventario

        for (i) in range(5):
            with open(archivo_inventario, 'rb') as archivo:
                # Configurar los datos del archivo
                archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                datos = {'parametro_adicional': 'valor_adicional'}

                # Definir el encabezado de autorización
                encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

                # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
                respuesta = requests.post(url_inventario, files=archivos, data=datos, headers=encabezado_autorizacion)
                json_response = json.loads(respuesta.text)

                if (json_response['success'] == True):
                    print(respuesta.text)
                    return json_response
                else:
                    print("Error al cargar el JSON INVENTARIO, Reintentando, Intento: ", i + 1)  
        return json_response
    except:
        return {"success": False, "message": "Error al cargar el JSON", "detail": "Error al cargar el JSON", "id":"1"}
