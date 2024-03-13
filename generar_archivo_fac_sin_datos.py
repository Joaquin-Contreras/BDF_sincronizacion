from datetime import datetime, timedelta
import pandas as pd
import os


fecha_archivos_menos_un_dia_str = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime("%Y%m%d")


def generar_archivo_fac_sin_datos():

    directorio_fac = "./XLSX_fac_done/"
    nombre_archivo_fac = "mendizabal_fac_" + fecha_archivos + ".xlsx"

    df = pd.DataFrame()

    df["IdDistribuidor"] = ""
    df["IdPaquete"] = ""
    df["Fecha"] = ""
    df["NroComprobante"] = ""
    df['IdPedidoDinesys'] = ""
    df["NroComprobanteAsociado"] = ""
    df["IdCliente"] = ""
    df['IdTipoDeCliente'] = ""
    df["IdVendedor"] = ""
    df["IdProducto"] = ""
    df['Cantidad'] = ""
    df["TipoDeComprobante"] = ""
    df["MotivoNC"] = ""

    ## SOLAPA VERIFICACIÓN ==>
    df_verificacion = pd.DataFrame()
    df_verificacion["IDICADOR"] = ["CantRegistros", "TotalCajas"]
    df_verificacion["VALOR"] = [0, 0]

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
