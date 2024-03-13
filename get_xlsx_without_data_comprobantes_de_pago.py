from datetime import datetime, timedelta
import pandas as pd
import os
import re


fecha_archivos_menos_un_dia_str = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime("%Y%m%d")

directorio_comprobantes_de_pago = "./XLSX_comprobantes_done"

nombre_archivo_comprobantes = re.sub(
    r"\s+", "_", "mendizabal_vta_" + fecha_archivos + ".xlsx"
)



def get_xlsx_without_data_comprobantes_de_pago():
    df = pd.DataFrame(
        columns=[
            "NroComprobante",
            "MotivoCR",
            "IdVendedor",
            "IdCliente",
            "IdTipoDeCliente",
            "Fecha",
            "IdPaquete",
            "IdProducto",
            "NroComprobanteAsociado",
            "TipoDocumento",
            "UnidadMedida",
            "Unidades",
            "IdDistribuidor",
            "Apellido",
            "Nombre",
        ]
    )
    df_verificacion = pd.DataFrame(
        data={"IDICADOR": ["CantRegistros", "TotalUnidades"], "VALOR": [0, 0]}
    )

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