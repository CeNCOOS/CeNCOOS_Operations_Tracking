import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ"
sheet = client.open_by_key(sheet_id)

# column B, row x (where x is the row number)
cell_value = sheet.sheet1.cell(3, 2).value
print(cell_value)