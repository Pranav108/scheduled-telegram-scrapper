import sys,os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import datetime
import gspread
import json
sys.path.append(os.getcwd())
from db.db_model import DynamoDB_con
DB = DynamoDB_con()

yesterday = datetime.date.today() - datetime.timedelta(days=1)
def refactor(obj):
    timeStamp=obj['DateTimeStamp'].split('.')[0]
    Success=obj['Success']
    JumbledWord_InitiatedByUser_ID=int(obj['JumbledWord_InitiatedByUser_ID'])
    JumbledWord_Participation=int(obj['JumbledWord_Participation'])
    return [timeStamp,JumbledWord_InitiatedByUser_ID,JumbledWord_Participation,Success]

# READING FROM DynamoDB
yesterday=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data('ST_JWB_Data',yesterday)
sheetData=list(map(refactor,sheetData))
# print(sheetData)

# with open('workSheet5/messageList.json') as f:
#    sheetData = json.load(f)
# for el in sheetData:
#     DB.send_data(el,'ST_JWB_Data')
# print('Data from JWB_DATA_DB')

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.get_worksheet(6)
worksheet.append_rows(sheetData)
print('scrapping in workSheet5 done, successfully')
