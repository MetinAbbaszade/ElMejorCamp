import os.path
from app.api.v1.schemas.sheet import SheetModel, updateSheetModel
from datetime import datetime
from fastapi import APIRouter, status
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from uuid import uuid4

router = APIRouter(prefix='/api/v1/sheet', tags=['sheets'])

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "183dZIelF1f0iFySm4QfCRYJyCKkUkP7kNWIMhJgWtAo"

@router.post('/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def add_to_sheet(Model: SheetModel):
    creds = None
    token_path = "token.json"
    credentials_path = "/Users/methiinn/Desktop/elmejor/backend/app/api/v1/schemas/credentials.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=3000, prompt="consent")

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A:A").execute()
        values = result.get("values", [])
        next_row = len(values) + 1 

        SAMPLE_RANGE_NAME = f"Sheet1!A{next_row}"
        id = uuid4()
        create_time = datetime.now()
        update_time = datetime.now()
        Model.id = str(id)
        Model.created_at = str(create_time)
        Model.updated_at = str(update_time)
        valueData = [[Model.parent_info, Model.parent_number, Model.player_info, Model.player_birth_date, \
            Model.player_adress, Model.player_club, Model.player_position, Model.player_strong_foot, Model.payment, Model.id, \
                Model.created_at, Model.updated_at]]
        result = (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", body={"values": valueData})
            .execute()
        )

    except HttpError as err:
        print(f"Google Sheets API error: {err}")


@router.put('/update-payment', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def update_payment(model: updateSheetModel):
    creds = None
    token_path = "token.json"
    credentials_path = "/Users/methiinn/Desktop/elmejor/backend/credentials.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=3000, prompt="consent")

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A:J").execute()
        values = result.get("values", [])

        row_to_update = None
        for index, row in enumerate(values, start=1):  
            if len(row) > 9 and str(row[9]) == model.id:  
                row_to_update = index
                break

        if row_to_update:
            update_range = f"Sheet1!I{row_to_update}"
            
            sheet.values().clear(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=update_range
            ).execute()

            value_data = [["Ödənilib"]]
            sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=update_range,
                valueInputOption="USER_ENTERED",
                body={"values": value_data}
            ).execute()

            print(f"Updated row {row_to_update} with 'Ödənilib'")
        else:
            print("User not found in the sheet.")

    except Exception as err:
        print(f"Google Sheets API error: {err}")