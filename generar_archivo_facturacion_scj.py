from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os


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

def generar_archivo_facturacion_scj():

    directorio_fac = "./XLSX_fac_done/"
    nombre_archivo_fac = "mendizabal_fac_" + fecha_archivos + ".xlsx"


    try:
        df_comprobantes_old = pd.read_csv(
            "./CSV_comprobantes_old/mendizabal_vta_" + fecha_real + ".csv",
            encoding="ISO-8859-1",
            delimiter="\t",
        )
    except UnicodeDecodeError:
        df_comprobantes_old = pd.read_csv(
            "./CSV_comprobantes_old/mendizabal_vta_" + fecha_real + ".csv",
            encoding="cp1252",
            delimiter="\t",
        )

    df = pd.DataFrame()
    valores_no_deseados = ['MINUTA DE INGRESO', 'ANTICIPO', 'NOTA DE DEBITO', 'RECIBO']

    df["IdDistribuidor"] = ["15426"] * len(df_comprobantes_old)
    df["IdPaquete"] = valorIdPaquete
    df["Fecha"] = pd.to_datetime(df_comprobantes_old["Fecha Comprobante"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    df["NroComprobante"] = df_comprobantes_old["Numero"]
    df['IdPedidoDinesys'] = 0
    df["NroComprobanteAsociado"] = np.where(
        df_comprobantes_old["Descripcion Comprobante"] == "NOTA DE CREDITO", df_comprobantes_old["Numero"], np.nan
    )
    df["IdCliente"] = df_comprobantes_old["Cliente"]
    df['IdTipoDeCliente'] = df_comprobantes_old['Subcanal']
    df['IdTipoDeCliente'] = df['IdTipoDeCliente'].replace({11: 8, 9: 8, 15: 8, 10: 8, 16: 8})
    df["IdVendedor"] = df_comprobantes_old["Vendedor"]
    df["IdProducto"] = df_comprobantes_old["Codigo de Articulo"]

    df['Cantidad'] = df_comprobantes_old['Unidades por Bulto'] * df_comprobantes_old['Bultos Total']

    df['TipoDeComprobante'] = ~df_comprobantes_old['Descripcion Comprobante'].isin(valores_no_deseados)
    df["TipoDeComprobante"] = np.where(
        df_comprobantes_old["Descripcion Comprobante"] == "NOTA DE CREDITO",
        "NC",
        np.where(df_comprobantes_old["Descripcion Comprobante"] == "NOTA DE DEBITO", "ND", "FC"),
    )
    df["MotivoNC"] = np.where(
        df_comprobantes_old["Descripcion Comprobante"] == "NOTA DE CREDITO",
        df_comprobantes_old["Motivo Rechazo / Devolucion"],
        np.nan,
    )

    df['Deposito'] = df_comprobantes_old['Deposito']
    df = df[df_comprobantes_old["Deposito"].apply(lambda x: x == 1)]
    df = df[df_comprobantes_old["PROVEEDORES"].apply(lambda x: (x == 1003) or (x == 1061))]

    df.drop(columns=['Deposito'], inplace=True)
    ## SOLAPA VERIFICACIÓN ==>
    df_verificacion = pd.DataFrame()
    suma_cantidad = df["Cantidad"].sum()
    # suma_cantidad = "{:,.2f}".format(suma_cantidad).replace(".", ",")
    df_verificacion["IDICADOR"] = ["CantRegistros", "TotalCajas"]
    df_verificacion["VALOR"] = [len(df), suma_cantidad]

    
    def format_with_comma(value):
        formatted_value = "{:,.2f}".format(value).replace('.', ',')
        return formatted_value


    # df['Cantidad'] = df['Cantidad'].apply(format_with_comma)
    # Convirtiendo DF a XLSX


    if not os.path.exists(directorio_fac):
        try:
            os.makedirs(directorio_fac)
            print(f"Directorio '{directorio_fac}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_fac}': {e}")

    if os.access(directorio_fac, os.W_OK):
        try:
            with pd.ExcelWriter(
                "./XLSX_fac_done/" + "" + nombre_archivo_fac,
                engine="openpyxl",
            ) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
            print(
                f"Archivo '{nombre_archivo_fac}' creado correctamente en '{nombre_archivo_fac}'."
            )
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_fac}': {e}")
    else:
        print(
            f"No tienes permisos para escribir en el directorio '{directorio_fac}'."
        )