import requests
import re
from datetime import datetime

fecha_archivos = datetime.now().strftime('%Y%m%d')


value = "Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=="


url_inventario = 'https://dev.BDFdistribuidores.com/ws/inv'
# directorio_inventario = "./XLSX_inventario_done/"

# nombre_archivo_inventario = 'mendizabal_inv_'+fecha_archivos+'.xlsx'

# archivo_inventario = directorio_inventario+nombre_archivo_inventario

# print(archivo_inventario)
# with open(archivo_inventario, 'rb') as archivo:
#     # Configurar los datos del archivo
#     archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
#     datos = {'parametro_adicional': 'valor_adicional'}

#     # Definir el encabezado de autorización
#     encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

#     # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
#     respuesta = requests.post(url_inventario, files=archivos, data=datos, headers=encabezado_autorizacion)


#     print(respuesta.text)




url_mc = "https://dev.BDFdistribuidores.com/ws/mc"
directorio_mc = "./XLSX_master_clientes_done/"

nombre_archivo_inventario = 'mendizabal_mc_'+fecha_archivos+'.xlsx'

archivo_inventario = directorio_mc+nombre_archivo_inventario

print(archivo_inventario)
with open(archivo_inventario, 'rb') as archivo:
    # Configurar los datos del archivo
    archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

    # Definir el encabezado de autorización
    encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

    # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
    respuesta = requests.post(url_mc, files=archivos, headers=encabezado_autorizacion)


    print(respuesta.text)


# url_mc = "https://dev.BDFdistribuidores.com/ws/vta"
# directorio_mc = "./XLSX_comprobantes_done/"

# nombre_archivo_inventario = 'mendizabal_vta_'+fecha_archivos+'.xlsx'

# archivo_inventario = directorio_mc+nombre_archivo_inventario

# print(archivo_inventario)
# with open(archivo_inventario, 'rb') as archivo:
#     # Configurar los datos del archivo
#     archivos = {'archivo': (nombre_archivo_inventario, archivo, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

#     # Definir el encabezado de autorización
#     encabezado_autorizacion = {'Authorization': 'Basic bWVuZGl6YWJhbDptZW5kaXphYmFsOTg1NA=='}

#     # Enviar la solicitud POST a la API con los archivos, los datos y el encabezado de autorización
#     respuesta = requests.post(url_mc, files=archivos, headers=encabezado_autorizacion)


#     print(respuesta.text)