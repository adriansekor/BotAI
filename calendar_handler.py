import datetime
import os
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account

BASE_DIR = Path(__file__).resolve().parent
SERVICE_ACCOUNT_FILE = str(BASE_DIR / 'botai-paco-07b7bfb4e75d.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'adrianmedranohervas@gmail.com'

def obtener_servicio():
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            return None
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('calendar', 'v3', credentials=creds)
    except Exception:
        return None

def leer_proximas_citas():
    service = obtener_servicio()
    if not service: return "L'agenda no està disponible."
    ahora = datetime.datetime.utcnow().isoformat() + 'Z'
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID, timeMin=ahora,
            maxResults=5, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events: return "No hi ha cites properes."
        resumen = ""
        for event in events:
            inicio = event['start'].get('dateTime', event['start'].get('date'))
            resumen += f"- {event['summary']} el {inicio}\n"
        return resumen
    except Exception as e:
        return f"Error llegint cites: {e}"

def crear_cita(resumen: str, fecha_hora_inicio: str):
    print(f"--- EXECUTANT FUNCIÓ REAL: crear_cita per a {resumen} ---")
    service = obtener_servicio()
    if not service: return "Error de connexió amb Google."
    try:
        fecha_neta = fecha_hora_inicio.replace('Z', '').replace(' ', 'T')
        inici_dt = datetime.datetime.fromisoformat(fecha_neta)
        fin_dt = inici_dt + datetime.timedelta(hours=1)
        evento = {
            'summary': resumen,
            'start': {'dateTime': inici_dt.isoformat(), 'timeZone': 'Europe/Madrid'},
            'end': {'dateTime': fin_dt.isoformat(), 'timeZone': 'Europe/Madrid'},
        }
        service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
        print("--- CITA CREADA AMB ÈXIT AL CALENDARI ---")
        return f"Confirmat: Cita creada per a {resumen}."
    except Exception as e:
        print(f"--- ERROR CREANT CITA: {e} ---")
        return f"Error al crear la cita: {e}"