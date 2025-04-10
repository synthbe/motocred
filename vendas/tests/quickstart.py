import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHEET_ID = os.getenv("SHEET_ID")

flow = InstalledAppFlow.from_client_config("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()
result = (
    sheet.values().get(spreadsheetId=SHEET_ID,).execute()
)

values = result.get("values", [])

print(values)
