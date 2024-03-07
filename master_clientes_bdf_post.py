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



def master_clientes_bdf_post():
    try:
        url_mc = "https://dev.BDFdistribuidores.com/ws/mc"
        # url_mc = "https://mendizabal.BDFdistribuidores.com/ws/mc"

        directorio_mc = "./XLSX_master_clientes_done/"

        nombre_archivo_mc = 'mendizabal_mc_'+fecha_archivos+'.xlsx'

        archivo_mc = directorio_mc+nombre_archivo_mc

        for (i) in range(5):
            with open(archivo_mc, 'rb') as archivo:
                # Configurar los datos del archivo
                # archivos = {'archivo': (nombre_archivo_mc, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                archivos = {'archivo': (nombre_archivo_mc, archivo, 'application/vnd.ms-excel')}

                # Definir el encabezado de autorización
                encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

                # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
                respuesta = requests.post(url_mc, files=archivos, headers=encabezado_autorizacion)

                json_response = json.loads(respuesta.text)

                if (json_response['success'] == True):
                    print(respuesta.text)
                    return json_response
                else:
                    print("Error al cargar el JSON MC, Reintentando, Intento:", i + 1)
        return json_response
    except:
        return {"success": False, "message": "Error al cargar el JSON", "detail": "Error al cargar el JSON", "id":"2"}
