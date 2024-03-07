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

def ventas_bdf_post():
    try:
        url_vta = "https://dev.BDFdistribuidores.com/ws/vta"
        # url_vta = "https://mendizabal.BDFdistribuidores.com/ws/vta"

        directorio_mc = "./XLSX_comprobantes_done/"

        nombre_archivo_ventas = 'mendizabal_vta_'+fecha_archivos+'.xlsx'

        archivo_ventas = directorio_mc+nombre_archivo_ventas

        for (i) in range(5):
            with open(archivo_ventas, 'rb') as archivo:
                # Configurar los datos del archivo
                archivos = {'archivo': (nombre_archivo_ventas, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

                # Definir el encabezado de autorización
                encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

                # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
                respuesta = requests.post(url_vta, files=archivos, headers=encabezado_autorizacion)

                json_response = json.loads(respuesta.text)


                if (json_response['success'] == True):
                    print(respuesta.text)
                    return json_response
                else:
                    print("Error al cargar el JSON VTA, Reintentando, Intento: ", i + 1)
        return json_response
    except:
        return {"success": False, "message": "Error al cargar el JSON", "detail": "Error al cargar el JSON", "id":"3"}

