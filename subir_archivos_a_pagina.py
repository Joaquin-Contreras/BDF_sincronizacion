import requests

def subir_archivos_a_pagina(ruta_archivo, nombre_carpeta):


    url = 'http://127.0.0.1:5000/upload' # ONLY TEST URL
    archivo =  ruta_archivo # 'C:/Users/SebastianFuhr/Desktop/BDF_sincronizaci/BDF_sincronizacion/XLSX_comprobantes_done/mendizabal_vta_20240329.xlsx'
    carpeta = nombre_carpeta # 'XLSX_comprobantes_done'

    files = {'file': open(archivo, 'rb')}
    data = {'folder': carpeta}

    response = requests.post(url, files=files, data=data)

    print(response.json())