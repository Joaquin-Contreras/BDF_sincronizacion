from datetime import datetime, timedelta
import pandas as pd
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

directorio_clientes = "./XLSX_clientes_dinesys_done/"
nombre_archivo_clientes = "clientes"

def generar_archivo_clientes_dinesys():

    ID_VENDEDORES = {
    "DANIEL JORGE": 1001,
    "ANTOÑANZAS MARTIN": 1003,
    "MENDOZA RODOLFO": 1006,
    "AGUIRRE VANESA": 1007,
    "JIMENEZ SOLIS": 1008,
    "DUERTO GABRIEL": 1011,
    "NACHO": 1012, # MENDIZABAL JUAN IGNACIO
    "MARCHESE ANDREA": 1018,
    "HEIDEL ROMINA": 1117,
    "MEDINA ROBERTO": 1118,
    "BONICALZI MARIANA": 1125,
    "SOMOZA MARIA SILVINA": 1127,
    "LEONARDO FASSI": 1132,
    "SANCHEZ DAMIAN": 1135,
    "PABLO BARCO": 1138,
    "VENTAS SIN VENDEDOR": 1999
    }

    df_varios = pd.read_excel("./varios/VARIOS_LIMPIO.xlsx")
    df_localidades = pd.read_excel('./XLSX_localidades_provincias/Localidades.xlsx', header=1)

    df_clientes_datos = pd.read_excel(
        "./CSV_clientes_old/mendizabal_mc_" + fecha_archivos + "_1.xlsx",
        sheet_name="Clientes",
        header=1,
        skiprows=[2],
    )

    df = pd.DataFrame()

    df['Código'] = df_clientes_datos['Cliente'].astype(int)
    df['Dirección'] = df_clientes_datos['Calle'] + " " + (df_clientes_datos['Altura'].astype(str))
    df['Razón social'] = df_clientes_datos['Razón social']

    df['Código de tipo de cliente'] = df_clientes_datos["Subcanal MKT"].replace({11: 8, 9: 8, 15: 8, 10: 8, 16: 8, 52:8, 12:8})

    def buscar_vendedor(texto):
        for vendedor in ID_VENDEDORES.keys():
            if re.search(r'\b' + re.escape(vendedor) + r'\b', texto):
                return ID_VENDEDORES[vendedor]
        return 1999
    
    df["Código de vendedor"] = df_clientes_datos['Descripción Ruta Vta.'].apply(buscar_vendedor)
    df['Código de zona / ruta'] = df_clientes_datos['Descripción Ruta Vta.'].apply(buscar_vendedor)
    df['Orden de visita'] = 0
    df['Codigo de lista de precios'] = 0
    df['Descuento'] = 0

    df_varios['DEPARTAMENTO'] = df_varios['DEPARTAMENTO'].str.strip()
    # Fusionar df_clientes_datos y df_localidades en función de "Código Localidad" e "ID"
    df_merge = pd.merge(df_clientes_datos, df_localidades, left_on='Código Localidad', right_on='Id', how='left')
    df_merge.rename(columns={'Departamento': 'DEPARTAMENTO'}, inplace=True)

    # Fusionar df_merge y df_varios en función de "Departamento"
    df_final = pd.merge(df_merge, df_varios, on='DEPARTAMENTO', how='left')

    # Seleccionar las columnas necesarias
    result = df_final[['Código Localidad', 'DEPARTAMENTO', 'CP']]


    df['Código Localidad'] = result['CP']


    if not os.path.exists(directorio_clientes):
        try:
            os.makedirs(directorio_clientes)
            print(f"Directorio '{directorio_clientes}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_clientes}': {e}")

    if os.access(directorio_clientes, os.W_OK):
        try:
            # Ruta del archivo CSV
            ruta_archivo_csv = "./XLSX_clientes_dinesys_done/" + nombre_archivo_clientes + ".csv"
            
            # Escribir el DataFrame en un archivo CSV
            df.to_csv(ruta_archivo_csv, index=False, header=False)

            print(f"Archivo '{nombre_archivo_clientes}.csv' creado correctamente en '{directorio_clientes}'.")
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_clientes}': {e}")
    else:
        print(
            f"No tienes permisos para escribir en el directorio '{directorio_clientes}'."
        )



###### COLUMNAS
    # Código => Columna: Cliente
    # Dirección => Columna: Calle + Altura
    # Razón social => Columna: Razón social
    # Código de tipo de cliente => Columna: Subcanal MKT
    # Código de vendedor => Columna: Descripción Ruta Vta. MATCHEAR CON ID_VENDEDORES
    # Orden de visita => ?? == 0
    # Codigo de lista de precios => 0
    # Descuento => 0
    # Codigo de localidad = Column2 (del archivo Varios.csv)