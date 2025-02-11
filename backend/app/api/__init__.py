# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError


# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


# SAMPLE_SPREADSHEET_ID = "183dZIelF1f0iFySm4QfCRYJyCKkUkP7kNWIMhJgWtAo"
# SAMPLE_RANGE_NAME = "Sheet1!A2"


# def main():
#   creds = None
#   if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#   if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#       creds.refresh(Request())
#     else:
#       flow = InstalledAppFlow.from_client_secrets_file(
#           "credentials.json", SCOPES
#       )
#       creds = flow.run_local_server(port=3000)
#     with open("token.json", "w") as token:
#       token.write(creds.to_json())

#   try:
#     service = build("sheets", "v4", credentials=creds)

#     valueData = [['Picler', 'Salam'], ['Chocolate'], ['Chips'], ['Sala']]
#     sheet = service.spreadsheets()
#     result = (
#         sheet.values()
#         .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED",  body={"values": valueData})
#         .execute()
#     )

#   except HttpError as err:
#     print(err)


# if __name__ == "__main__":
#   main()