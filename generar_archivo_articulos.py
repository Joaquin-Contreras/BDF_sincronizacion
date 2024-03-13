from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import re

fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
# fecha_formateada = (fecha_actual).strftime("%d de %B de %Y")
# La línea 8 está solamente para hacer pruebas, la línea 6 es la correspondiente
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1


months = {
    "January": "enero",
    "February": "febrero",
    "March": "marzo",
    "April": "abril",
    "May": "mayo",
    "June": "junio",
    "August": "agosto",
    "September": "septiembre",
    "October": "octubre",
    "November": "noviembre",
    "December": "diciembre",
}
month = fecha_formateada.split(" de ")[1].split(" de ")[0]

if month in months:
    mes = months[month]
    fecha_real = fecha_formateada.replace(month, mes)

if fecha_real[0] == "0":
    fecha_real = fecha_real[1:]

fecha_archivos_menos_un_dia_str = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime("%Y%m%d")

directorio_articulos = './XLSX_articulos_dinesys'

nombre_archivo_articulos = 'articulos'


def generar_archivo_articulos():

    df_inventario = pd.read_excel("./XLSX_inv_dinesys_old/inv_dinesys_old" + fecha_archivos + ".xlsx", header=1)

    df_inventario = df_inventario.drop([0])

    # Restablece los índices
    df_inventario.reset_index(drop=True, inplace=True)

    df = pd.DataFrame()

    df['Código sinónimo'] = df_inventario['Código']
    df['Codigo SG'] = df_inventario['Cod.Artículo Proveedor']
    df['Descripción'] = df_inventario['Descripción']
    df['Unidades x Bulto'] = df_inventario['Unidad x Bulto']
    df['Código de rubro'] = 1 # Todo en aire
    df['Pertenece a SCJ'] = 1
    df['Stock'] = 0


    if not os.path.exists(directorio_articulos):
        try:
            os.makedirs(directorio_articulos)
            print(f"Directorio '{directorio_articulos}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_articulos}': {e}")

    if os.access(directorio_articulos, os.W_OK):
        try:
            # Ruta del archivo CSV
            ruta_archivo_csv = "./XLSX_articulos_dinesys/" + nombre_archivo_articulos + ".csv"
            
            # Escribir el DataFrame en un archivo CSV
            df.to_csv(ruta_archivo_csv, index=False, header=False)

            print(f"Archivo '{nombre_archivo_articulos}.csv' creado correctamente en '{directorio_articulos}'.")
        except Exception as e:
            print(f"Error al crear el archivo CSV: {str(e)}")
    else:
        print(
            f"No tienes permisos para escribir en el directorio '{directorio_articulos}'."
        )