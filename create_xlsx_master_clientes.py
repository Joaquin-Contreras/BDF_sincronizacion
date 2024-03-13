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


fecha_archivos_menos_un_dia_str = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime("%Y%m%d")


directorio_master_clientes = "./XLSX_master_clientes_done"

nombre_archivo_master_clientes = re.sub(
    r"\s+", "_", "mendizabal_mc_" + fecha_archivos + ".xlsx"
)




def create_xlsx_master_clientes():
    equivalencias = {
        "SPM Y AUTOS. CHICO": 1,
        "MAYORISTAS": 2,
        "PERF. Y CASA DE ART LIMP.": 3,
        "DROGUERIAS": 4,
        "FERRETERIAS": 5,
        "FARMACIA": 6,
        "KIOSCOS Y EESS": 7,
        "OTROS": 8,
        "SPM Y AUTOS. MEDIANO": 21,
        "SPM Y AUTOS. GRANDE": 22,
        "ALMACENES": 23,
        "SUCURSALES": 24,
        "VACANTE": 52,
        "DISTRIDIGITAL": 53,
        "PROFESSIONAL": 54,
        "CADENAS REGIONALES": 55,
    }
    provincias = {
        "CAPITAL FEDERAL": 2,
        "BUENOS AIRES": 6,
        "CATAMARCA": 10,
        "CORDOBA": 14,
        "CORRIENTES": 18,
        "CHACO": 22,
        "CHUBUT": 26,
        "ENTRE RIOS": 30,
        "FORMOSA": 34,
        "JUJUY": 38,
        "LA PAMPA": 42,
        "LA RIOJA": 46,
        "MENDOZA": 50,
        "MISIONES": 54,
        "NEUQUEN": 58,
        "RIO NEGRO": 62,
        "SALTA": 66,
        "SAN JUAN": 70,
        "SAN LUIS": 74,
        "SANTA CRUZ": 78,
        "SANTA FE": 82,
        "SANTIAGO DEL ESTERO": 86,
        "TUCUMAN": 90,
        "TIERRA DEL FUEGO": 94,
    }


    # Creando Solapa Datos ========>
    df_clientes_datos = pd.read_excel(
        "./CSV_clientes_old/mendizabal_mc_" + fecha_archivos + "_1.xlsx",
        sheet_name="Clientes",
        header=1,
        skiprows=[2],
    )

    df_jerarquiaMKT_datos = pd.read_excel(
        "./CSV_clientes_old/mendizabal_mc_" + fecha_archivos + "_1.xlsx",
        sheet_name="Jerarquía MKT",
        header=1,
    )

    df_localidades = pd.read_excel(
        "XLSX_localidades_provincias/Localidades.xlsx",
        sheet_name="Localidades",
        header=1,
    )

    df = pd.DataFrame()
    df["IdDistribuidor"] = [40379573] * len(df_clientes_datos)

    df["IdPaquete"] = valorIdPaquete

    df["IdCliente"] = df_clientes_datos["Cliente"]
    df["RazonSocial"] = df_clientes_datos["Razón social"]
    df["BannerText"] = ""

    df_merged_prov = pd.DataFrame()
    df_merged_prov["codigo_localidad"] = df_clientes_datos["Código Localidad"]
    codigo_to_provincia = dict(zip(df_localidades["Id"], df_localidades["Provincia"]))
    df_merged_prov["Provincia"] = df_merged_prov["codigo_localidad"].map(
        codigo_to_provincia
    )
    df["IdProvincia"] = pd.to_numeric(
        df_merged_prov["Provincia"].map(provincias), errors="coerce"
    )

    df["Localidad"] = df_clientes_datos["Código Localidad"]
    df_merged_l = pd.DataFrame()
    df_merged_l["codigo_localidad"] = df_clientes_datos["Código Localidad"]
    codigo_to_localidad = dict(zip(df_localidades["Id"], df_localidades["Localidad"]))
    df_merged_l["Localidad"] = df_merged_l["codigo_localidad"].map(codigo_to_localidad)
    df["Localidad"] = df["Localidad"].map(df_merged_l["Localidad"])

    df_merged_cp = pd.DataFrame()
    df_merged_cp["codigo_localidad"] = df_clientes_datos["Código Localidad"]
    codigo_to_cp = dict(zip(df_localidades["Id"], df_localidades["Código Postal"]))
    df_merged_cp["CodigoPostal"] = df_merged_cp["codigo_localidad"].map(codigo_to_cp)
    df["CodigoPostal"] = (df_merged_cp["CodigoPostal"]).astype(int).replace(",", ".")

    df["Calle"] = df_clientes_datos["Calle"]
    df["Numero"] = df_clientes_datos["Altura"]
    df["CUIT"] = df_clientes_datos["Identificador"].astype(str)
    df["Latitud"] = df_clientes_datos["Latitud"]
    df["Longitud"] = df_clientes_datos["Longitud"]

    df_merged = pd.DataFrame()
    # Agregamos la columna 'Subcanal MKT' de df1 al nuevo DataFrame
    df_merged["Subcanal MKT"] = df_clientes_datos["Subcanal MKT"]
    # Creamos un diccionario para mapear los valores de 'Código' en df1 con los valores correspondientes de 'Subcanal MKT' en df2
    codigo_to_subcanal = dict(
        zip(df_jerarquiaMKT_datos["Código"], df_jerarquiaMKT_datos["Subcanal MKT"])
    )
    # Mapeamos los valores de 'Código' en df1 con los valores correspondientes de 'Subcanal MKT' en df2
    df_merged["Subcanal MKT"] = df_merged["Subcanal MKT"].map(codigo_to_subcanal)
    df["IdTipoCliente"] = df_merged["Subcanal MKT"].map(equivalencias)

    df = df.dropna(subset=["IdTipoCliente"])
    df = df.dropna(subset=["Localidad"])
    df["IdTipoCliente"] = (df["IdTipoCliente"]).astype(int)
    df = df[df["CUIT"].apply(lambda x: len(str(x)) >= 11)]
    df["RazonSocial"] = df["RazonSocial"].apply(
        lambda x: re.sub(r"\([^)]*\)", "", str(x))
    )
    # df.reset_index(drop=True, inplace=True)

    # <======== Creando Solapa Datos

    # CREANDO SOLAPA verificacion =====>
    total_registros = len(df)
    data = {"IDICADOR": ["CantRegistros"]}
    df_verificacion = pd.DataFrame(data)
    df_verificacion["VALOR"] = [total_registros]
    # <===== CREANDO SOLAPA verificacion

    if not os.path.exists(directorio_master_clientes):
        try:
            os.makedirs(directorio_master_clientes)
            print(f"Directorio '{directorio_master_clientes}' creado correctamente.")
        except OSError as e:
            print(f"No se pudo crear el directorio '{directorio_master_clientes}': {e}")

    if os.access(directorio_master_clientes, os.W_OK):
        try:
            with pd.ExcelWriter(
                "./XLSX_master_clientes_done/" + "" + nombre_archivo_master_clientes,
                engine="openpyxl",
            ) as writer:
                df.to_excel(writer, sheet_name="datos", index=False)
                df_verificacion.to_excel(writer, sheet_name="verificacion", index=False)
            print(
                f"Archivo '{nombre_archivo_master_clientes}' creado correctamente en '{directorio_master_clientes}'."
            )
        except Exception as e:
            print(f"Error al crear el archivo '{nombre_archivo_master_clientes}': {e}")
    else:
        print(
            f"No tienes permisos para escribir en el directorio '{directorio_master_clientes}'."
        )