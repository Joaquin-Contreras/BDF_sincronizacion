import requests
from datetime import datetime, timedelta
import json
import pandas as pd


# value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="

def fac_scj_post(urls, archivos_a_reenviar, dias_a_restar):

    fecha_archivos_menos_un_dia_str  = datetime.now()
    fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=dias_a_restar)
    fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')

    try:
        url_fac = urls['fac_scj']
        directorio_fac = "./XLSX_fac_done/"
        json_response = {"success": False, "message": "No se enviaron archivos", "detail": "No se encontraron archivos para enviar", "id": "0"}

        if archivos_a_reenviar:
            for nombre_archivo in archivos_a_reenviar:
                archivo_facturacion = directorio_fac + nombre_archivo
                try:
                    with open(archivo_facturacion, 'rb') as archivo:
                        archivos = {'archivo': (nombre_archivo, archivo, 'application/vnd.ms-excel')}
                        datos = {'parametro_adicional': 'valor_adicional'}
                        encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

                        respuesta = requests.post(url_fac, files=archivos, data=datos, headers=encabezado_autorizacion)
                        try:
                            json_response = json.loads(respuesta.text)
                        except:
                            print("Error al cargar el JSON FAC, Reintentando")

                        if json_response['success']:
                            json_response['archivo_reenviado'] = nombre_archivo
                            print("Archivo reenviado:", nombre_archivo)
                            print(respuesta.text)
                            eliminar_fila_reenvio(nombre_archivo)
                            break
                        else:
                            print("Error: " + json_response['message'])
                except:
                    print("El archivo que intenta abrir no existe o no está en esa ruta")
                    break
        else:
            print("No hay archivos para reenviar")
        
        nombre_archivo_facturacion = 'mendizabal_fac_'+fecha_archivos+'.xlsx'
        archivo_facturacion = directorio_fac + nombre_archivo_facturacion
        trying = 0
        while trying <= 5:
            try:
                with open(archivo_facturacion, 'rb') as archivo:
                    archivos = {'archivo': (nombre_archivo_facturacion, archivo, 'application/vnd.ms-excel')}
                    datos = {'parametro_adicional': 'valor_adicional'}
                    encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

                    respuesta = requests.post(url_fac, files=archivos, data=datos, headers=encabezado_autorizacion)
                    try:
                        json_response = json.loads(respuesta.text)
                    except:
                        print("Error al cargar el JSON FAC, Reintentando")

                    if json_response['success']:
                        print(respuesta.text)
                        return json_response
                    else:
                        print("Error: " + json_response['message'])
                        trying += 1
                        print("Reintentando", trying)
            except:
                print("El archivo que intenta abrir no existe o no está en esa ruta")
                break

        return json_response

    except Exception as e:
        print(f"Error en la función fac_scj_post: {e}")
        return {"success": False, "message": "Error al cargar el JSON", "detail": str(e), "id": "1"}



def eliminar_fila_reenvio(nombre_archivo):
    try:
        archivo_reenvios = 'reenvios/reenvios_SCJ.xlsx'
        df_reenvios = pd.read_excel(archivo_reenvios)
        df_reenvios = df_reenvios[df_reenvios['nombre_archivo'] != nombre_archivo]
        df_reenvios.to_excel(archivo_reenvios, index=False)
        print(f"Fila correspondiente al archivo {nombre_archivo} eliminada del archivo de reenvíos.")
    except Exception as e:
        print(f"Error al intentar eliminar la fila correspondiente al archivo {nombre_archivo} del archivo de reenvíos: {e}")






# def fac_scj_post(urls, archivos_a_reenviar):
#     try:
#         url_fac = urls['fac_scj']

#         directorio_fac = "./XLSX_fac_done/"

#         nombre_archivo_facturacion = 'mendizabal_fac_'+fecha_archivos+'.xlsx'

#         archivo_facturacion = directorio_fac+nombre_archivo_facturacion
#         print(archivo_facturacion)
#         trying = 0
#         while trying <= 5:
#             try:
#                 with open(archivo_facturacion, 'rb') as archivo:
#                     # Configurar los datos del archivo
#                     archivos = {'archivo': (nombre_archivo_facturacion, archivo, 'application/vnd.ms-excel')}

#                     datos = {'parametro_adicional': 'valor_adicional'}

#                     # Definir el encabezado de autorización
#                     encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

#                     try:
#                     # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
#                         respuesta = requests.post(url_fac, files=archivos, data=datos, headers=encabezado_autorizacion)
#                     except requests.exceptions.RequestException as e:
#                         print("Error en la solicitud POST:", e)
                        
#                     try:
#                         json_response = json.loads(respuesta.text)
#                     except:
#                         print("Error al cargar el JSON FAC, Reintentando")


#                     if (json_response['success'] == True):
#                         print(respuesta.text)
#                         trying = 10
#                         return json_response
#                     else:
#                         print("Error: " + json_response['message'])
#                         trying += 1
#                         print("Reintentando", trying)
#             except: 
#                 print("El archivo que intenta abrir no existe o no está en esa ruta")
#                 break

#         return json_response
#     except:
#         return {"success": False, "message": "Error al cargar el JSON", "detail": "Error al cargar el JSON", "id":"1"}