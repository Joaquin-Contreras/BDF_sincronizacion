import requests
from datetime import datetime, timedelta
import json
import pandas as pd


    

def master_clientes_bdf_post(urls, archivos_a_reenviar, dias_a_restar):

    fecha_archivos_menos_un_dia_str  = datetime.now()
    fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=dias_a_restar)
    fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
    
    try:
        url_mc = urls['mc_bdf']
        directorio_mc = "./XLSX_master_clientes_done/"
        json_response = {"success": False, "message": "No se enviaron archivos", "detail": "No se encontraron archivos para enviar", "id": "0"}

        if archivos_a_reenviar:
            for nombre_archivo in archivos_a_reenviar:
                archivo_mc = directorio_mc + nombre_archivo

                try:
                    with open(archivo_mc, 'rb') as archivo:
                        # Configurar los datos del archivo
                        archivos = {'archivo': (nombre_archivo, archivo, 'application/vnd.ms-excel')}

                        # Definir el encabezado de autorización
                        encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

                        # Enviar la solicitud POST a la API con los archivos y el encabezado de autorización
                        respuesta = requests.post(url_mc, files=archivos, headers=encabezado_autorizacion)
                        try:
                            json_response = json.loads(respuesta.text)
                        except:
                            print("Error al cargar el JSON, Reintentando")

                        if json_response['success']:
                            json_response['archivo_reenviado'] = nombre_archivo
                            print("Archivo reenviado:", nombre_archivo)
                            print(respuesta.text)
                            # Eliminar la fila correspondiente del archivo de reenvíos
                            eliminar_fila_reenvio(nombre_archivo)
                            break
                        else:
                            print("Error: " + json_response['message'])

                except:
                    print("El archivo que intenta abrir no existe o no está en esa ruta")
                    break
        else:
            print("No hay archivos para reenviar")

        # Intentar enviar el archivo actual
        try:
            nombre_archivo_mc = f'mendizabal_mc_{fecha_archivos}.xlsx'
            archivo_mc = directorio_mc + nombre_archivo_mc

            trying = 0
            while trying <= 5:
                try:
                    with open(archivo_mc, 'rb') as archivo:
                        # Configurar los datos del archivo
                        archivos = {'archivo': (nombre_archivo_mc, archivo, 'application/vnd.ms-excel')}
                        encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}
                        respuesta = requests.post(url_mc, files=archivos, headers=encabezado_autorizacion)
                        try:
                            json_response = json.loads(respuesta.text)
                        except:
                            print("Error al cargar el JSON, Reintentando")

                        if json_response['success']:
                            print("Archivo DIARIO enviado exitosamente")
                            print(respuesta.text)
                            trying = 10
                            return json_response
                        else:
                            print("Error: " + json_response['message'])
                            trying += 1
                            print("Reintentando", trying)
                except:
                    print("El archivo que intenta abrir no existe o no está en esa ruta")
                    break

            return json_response
        except:
            return {"success": False, "message": "Error al cargar el JSON", "detail": "Error al cargar el JSON", "id": "2"}

    except Exception as e:
        print(f"Error en la función master_clientes_bdf_post: {e}")
        return {"success": False, "message": "Error al cargar el JSON", "detail": str(e), "id": "2"}

def eliminar_fila_reenvio(nombre_archivo):
    try:
        archivo_reenvios = 'reenvios/reenvios_BDF.xlsx'
        df_reenvios = pd.read_excel(archivo_reenvios)
        df_reenvios = df_reenvios[df_reenvios['nombre_archivo'] != nombre_archivo]
        df_reenvios.to_excel(archivo_reenvios, index=False)
        print(f"Fila correspondiente al archivo {nombre_archivo} eliminada del archivo de reenvíos.")
    except Exception as e:
        print(f"Error al intentar eliminar la fila correspondiente al archivo {nombre_archivo} del archivo de reenvíos: {e}")