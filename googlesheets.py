import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('PlacementPortal.json', scope)
client = gspread.authorize(creds)

def make_entry(applied,comp_info):
    try:
        print("here2")
        sh = client.open(comp_info.get('company'))
        sheet = sh.sheet1
        #row = ["ID","Name","Email","Branch","CGPA"]
        row = [applied.get("id"),applied.get("name"),applied.get("email"),applied.get("branch"),applied.get("cgpa")]
        sheet.insert_row(row)
        
    except:
        print("here1")
        sh = client.create(comp_info.get('company'))
        sheet=sh.sheet1
        row = ["ID","Name","Email","Branch","CGPA"]
        sheet.insert_row(row)
        row = [applied.get("id"),applied.get("name"),applied.get("email"),applied.get("branch"),applied.get("cgpa")]
        sheet.insert_row(row)
        sh.share(comp_info.get('email'),with_link=True,email_message="Please Find the Link for google spreadsheet containing the list of eligible and interested students")


