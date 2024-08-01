from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID = '1AeFzyh4I6vC2QoA2TuuRNqUpKDdJU-LeqCPYHODlF3s'

def leerGoogleSheets(name_hoja):
    
    creds = None
    # Cargar las credenciales desde el archivo JSON
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
    
    # Construir el servicio de la API de Google Sheets
    service = build('sheets', 'v4', credentials=creds)
    
    # Obtener la información de la hoja de cálculo
    sheets_response = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    
    # Obtener la lista de hojas
    sheets = sheets_response.get('sheets', [])
    alumnos_sheet_name = name_hoja  # Nombre exacto de la hoja que queremos leer

    # Buscar la hoja con el nombre específico
    for sheet in sheets:
        if sheet.get('properties', {}).get('title') == alumnos_sheet_name:
            break
    else:
        raise ValueError(f"No se encontró la hoja '{alumnos_sheet_name}' en el archivo de hoja de cálculo.")

    # Definir el rango de celdas a leer
    range_ = f'{alumnos_sheet_name}!A1:XFD'

    # Obtener los datos de la hoja
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
    
    # Extraer los valores de la respuesta
    values = result.get('values', [])

    return values

def cargar_hoja():
    creds = None
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheets_response = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheets_response.get('sheets', [])
    return sheets

import os
import shutil
import pandas as pd
from docxtpl import DocxTemplate,InlineImage
from docx.shared import Mm
# rutas
OUT_PATH = 'certificate/alumnosCertificados/' 

def deleteFile(path):
    if(os.path.exists(path)):
        shutil.rmtree(path)
    # create the file exit
    os.mkdir(OUT_PATH)



def createCertificate(data_list):
    # Obtener los encabezados y los datos
    headers = data_list[0]
    data_rows = data_list[1:]

    # Transformar los datos en diccionarios
    data_dicts = [dict(zip(headers, row)) for row in data_rows]

    try:
        # Crear certificados para cada conjunto de datos
        for data in data_dicts:
            try:
                plat_docx = DocxTemplate('documents/cerificado_base.docx')  # Cargar la plantilla del documento
                
                context = {
                    'codigo': data.get('CODIGO', ''),
                    'nombres': data.get('NOMBRES', ''),
                    'apellidos': data.get('APELLIDOS', ''),
                    'tema': data.get('TEMA', ''),
                    'inicio': data.get('FECHA DE INICIO', ''),
                    'fin': data.get('FECHA DE FIN', ''),
                    'horas': data.get('HORAS ACADEMICAS', ''),
                }
                
                plat_docx.render(context)  # Renderizar la plantilla con el contexto
                
                # Guardar el certificado con un nombre único
                output_path = f'certificadosAlumnos/certificado_{data.get("CODIGO", "sin_codigo")}.docx'
                plat_docx.save(output_path)
            except Exception as e:
                print(f"Error al procesar el certificado para {data.get('CODIGO', 'desconocido')}: {e}")

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Error inesperado: {e}"
    
    return 'LOS CERTIFICADOS SE CREARON CON EXITO...'

