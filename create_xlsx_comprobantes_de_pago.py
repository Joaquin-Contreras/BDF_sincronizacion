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


directorio_comprobantes_de_pago = "./XLSX_comprobantes_done"

nombre_archivo_comprobantes = re.sub(
    r"\s+", "_", "mendizabal_vta_" + fecha_archivos + ".xlsx"
)



def create_xlsx_comprobantes_de_pago():
    def asignar_tipo_documento(descripcion):
        if descripcion == "NOTA DE CREDITO":
            return "CR"
        elif descripcion == "NOTA DE DEBITO":
            return "DE"
        else:
            return "OR"
    valores_no_deseados = ['MINUTA DE INGRESO', 'ANTICIPO', 'NOTA DE DEBITO', 'RECIBO']

    # CREANDO SOLAPA datos ====>
    # TRANSFORMAR CSV A XLSX
    try:
        df_csv_old = pd.read_csv(
            "./CSV_comprobantes_old/mendizabal_vta_" + fecha_real + ".csv",
            encoding="ISO-8859-1",
            delimiter="\t",
        )
    except UnicodeDecodeError:
        df_csv_old = pd.read_csv(
            "./CSV_comprobantes_old/mendizabal_vta_" + fecha_real + ".csv",
            encoding="cp1252",
            delimiter="\t",
        )
    # Seleccionando las columnas que voy a necesitar
    df = df_csv_old[
        [
            "Descripcion Comprobante",
            "Numero",
            "Descripcion Motivo Rechazo / Devolucion",
            "Vendedor",
            "Descripcion Vendedor",
            "Cliente",
            "Subcanal",
            "Codigo de Articulo",
            "Unidades",
            "Fecha Comprobante",
            "PROVEEDORES",
        ]
    ]  # 'Comprobante'
    # 'Descripción PROVEEDORES'
    # Renombrando columnas
    df.rename(
        columns={
            "Cliente": "IdCliente",
            "Subcanal": "IdTipoDeCliente",
            "Vendedor": "IdVendedor",
            "Fecha Comprobante": "Fecha",
            "Unidades": "Cantidad",
            "Numero": "NroComprobante",
            "Descripcion Motivo Rechazo / Devolucion": "MotivoCR",
            "Codigo de Articulo": "IdProducto",
        },
        inplace=True,
    )

    # Agregando columnas necesarias
    df["IdDistribuidor"] = 40379573
    df["UnidadMedida"] = "PC"

    df["IdPaquete"] = valorIdPaquete
    df["IdPaquete"] = df["IdPaquete"].astype(int)

    df[["ApellidoVendedor", "NombreVendedor"]] = df["Descripcion Vendedor"].str.split(
        n=1, expand=True
    )
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    # Aplicar la función a la columna 'Descripcion Comprobante' para crear la nueva columna 'TipoDocumento'
    df['TipoDocumento'] = ~df['Descripcion Comprobante'].isin(valores_no_deseados)
    df["TipoDocumento"] = df["Descripcion Comprobante"].apply(asignar_tipo_documento)
    df["NroComprobanteAsociado"] = np.where(
        df["Descripcion Comprobante"] == "NOTA DE CREDITO", df["NroComprobante"], np.nan
    )
    df.drop("Descripcion Vendedor", axis=1, inplace=True)
    df.drop("Descripcion Comprobante", axis=1, inplace=True)

    df = df[
        [
            "IdDistribuidor",
            "IdPaquete",
            "IdCliente",
            "IdTipoDeCliente",
            "IdVendedor",
            "NombreVendedor",
            "ApellidoVendedor",
            "IdProducto",
            "UnidadMedida",
            "Fecha",
            "TipoDocumento",
            "Cantidad",
            "NroComprobante",
            "NroComprobanteAsociado",
            "MotivoCR",
        ]
    ]

    df = df[df["IdProducto"].apply(lambda x: x > 0)]
    df = df[(df["TipoDocumento"] != "CR") | (df["Cantidad"] != 0)]
    df['IdTipoDeCliente'] = df['IdTipoDeCliente'].replace({11: 8, 9: 8, 15: 8, 10: 8, 16: 8, 52:8, 12:8})
    df["PROVEEDORES"] = df_csv_old["PROVEEDORES"]
    df['Cantidad'] = (df_csv_old['Unidades por Bulto'] * df_csv_old['Bultos Cerrados']) + df_csv_old['Unidades']
    df['Deposito'] = df_csv_old['Deposito']	
    df = df[df["PROVEEDORES"].apply(lambda x: x == 1004)]
    df = df[df["Deposito"].apply(lambda x: x == 1)]
    df = df[df['TipoDocumento'].apply(lambda x: x != "DE")]





    df['IdProducto'] = df['IdProducto'].replace(850882, 85088)
    df['IdProducto'] = df['IdProducto'].replace(850772, 85077)
    df['IdProducto'] = df['IdProducto'].replace(852862, 85286)
    df['IdProducto'] = df['IdProducto'].replace(880012, 88001)
    df['IdProducto'] = df['IdProducto'].replace(850612, 85061)
    df['IdProducto'] = df['IdProducto'].replace(850632, 85063)
    df['IdProducto'] = df['IdProducto'].replace(850662, 85066)


    try:
        df.drop("Deposito", axis=1, inplace=True)
        df.drop("PROVEEDORES", axis=1, inplace=True)
    except:
        pass

    if not os.path.exists(directorio_comprobantes_de_pago):
        try:
            os.makedirs(directorio_comprobantes_de_pago)
            print(
                f"Directorio '{directorio_comprobantes_de_pago}' creado correctamente."
            )
        except OSError as e:
            print(
                f"No se pudo crear el directorio '{directorio_comprobantes_de_pago}': {e}"
            )
    # <=====     CREANDO SOLAPA datos
    # CREANDO SOLAPA verificacion =====>
            
    total_registros = len(df)
    suma_cantidad = df["Cantidad"].sum()
    data = {"IDICADOR": ["CantRegistros", "TotalUnidades"]}
    df_verificacion = pd.DataFrame(data)
    df_verificacion["VALOR"] = [total_registros, suma_cantidad]
    # <===== CREANDO SOLAPA verificacion


    # Convirtiendo DF a XLSX y creando la solapa datos
    if os.access(directorio_comprobantes_de_pago, os.W_OK):
        try:
            with pd.ExcelWriter(
                "./XLSX_comprobantes_done/" + "" + nombre_archivo_comprobantes
            ) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
            print(
                f"Archivo '{nombre_archivo_comprobantes}' creado correctamente en '{directorio_comprobantes_de_pago}'."
            )
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_comprobantes}': {e}")
    else:
        print(
            f"No tienes permisos para escribir en el directorio '{directorio_comprobantes_de_pago}'."
        )