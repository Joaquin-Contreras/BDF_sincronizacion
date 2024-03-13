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


def fac_scj_post(urls):
    try:
        url_fac = urls['fac_scj']

        directorio_fac = "./XLSX_fac_done/"

        nombre_archivo_facturacion = 'mendizabal_fac_'+fecha_archivos+'.xlsx'

        archivo_facturacion = directorio_fac+nombre_archivo_facturacion

        with open(archivo_facturacion, 'rb') as archivo:
            # Configurar los datos del archivo
            archivos = {'archivo': (nombre_archivo_facturacion, archivo, 'application/vnd.ms-excel')}

            datos = {'parametro_adicional': 'valor_adicional'}

            # Definir el encabezado de autorización
            encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

            # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
            respuesta = requests.post(url_fac, files=archivos, data=datos, headers=encabezado_autorizacion)

            try:
                json_response = json.loads(respuesta.text)
            except:
                print("Error al cargar el JSON FAC, Reintentando")


            if (json_response['success'] == True):
                print(respuesta.text)
                return json_response
            else:
                print("Error: " + json_response['message'])

        return json_response
    except:
        return {"success": False, "message": "Error al cargar el JSON", "detail": "Error al cargar el JSON", "id":"1"}
