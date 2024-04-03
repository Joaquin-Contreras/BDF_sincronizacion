from datetime import datetime, timedelta
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import uuid

id_unico = uuid.uuid4()
fecha_archivos_menos_un_dia_str  = datetime.now()
fecha_archivos_menos_un_dia = fecha_archivos_menos_un_dia_str - timedelta(days=1)
fecha_archivos = fecha_archivos_menos_un_dia.strftime('%Y%m%d')
fecha_datetime = pd.to_datetime(fecha_archivos).strftime('%Y-%m-%d')
hora_actual = datetime.now()
hora_formateada = hora_actual.strftime('%H-%M-%S')

fecha_inicio = datetime(2024, 2, 15)  # La fecha de inicio es el 15/2/24
fecha_actual = datetime.now()
fecha_formateada = (fecha_actual - timedelta(days=1)).strftime("%d de %B de %Y")
diferencia_dias = (fecha_actual - fecha_inicio).days
valorIdPaquete = diferencia_dias + 1

json_inv = None
json_mc = None
json_vta = None

def enviar_correos(destinatario, data):
    try:
        # Configuración del servidor SMTP
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'joacontre0@gmail.com'
        smtp_password = 'pyjp fwuv fxye osyv'

        # Crear instancia de conexión SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = 'joacontre0@gmail.com'
        msg['To'] = destinatario
        msg['Subject'] = 'ENVÍO DE ARCHIVOS'

        # Cuerpo del mensaje
        body = f"HOLA, {data} EJECUTADO EXITOSAMENTE"
        
        msg.attach(MIMEText(body, 'plain'))

        # archivos_adjuntos = [
        #     "./XLSX_inventario_done/mendizabal_inv_"+fecha_archivos+".xlsx",
        #     "./XLSX_comprobantes_done/mendizabal_vta_"+fecha_archivos+".xlsx",
        #     "./XLSX_master_clientes_done/mendizabal_mc_"+fecha_archivos+".xlsx",
        #     # "./XLSX_inventario_done_scj/mendizabal_inv_"+fecha_archivos+".xlsx",
        #     # "./XLSX_fac_done/mendizabal_fac_"+fecha_archivos+".xlsx",
        #     "./respuestas/respuesta.xlsx"
        # ]

        # for archivo in archivos_adjuntos:
        #     attachment = open(archivo, 'rb')

        #     part = MIMEBase('application', 'octet-stream')
        #     part.set_payload((attachment).read())
        #     encoders.encode_base64(part)
        #     part.add_header('Content-Disposition', f'attachment; filename= {archivo}')
            
        #     msg.attach(part)

        # Enviar correo electrónico
        server.send_message(msg)

        # Cerrar conexión SMTP
        server.quit()
        print("El correo se envió exitosamente")
    except Exception as e: 
        print("Error al enviar el correo, Error: ", e)
