from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account


def leerGoogleSheets(name_hoja):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    KEY = 'key.json'
    SPREADSHEET_ID = '1AeFzyh4I6vC2QoA2TuuRNqUpKDdJU-LeqCPYHODlF3s'
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
