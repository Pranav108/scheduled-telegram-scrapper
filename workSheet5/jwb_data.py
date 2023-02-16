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
    timeStamp=obj['Datetime'].split('.')[0]
    Success='N'
    JumbledWord_InitiatedByUser_ID=int(obj['JumbledWord_InitiatedByUser_ID'])
    JumbledWord_Participation=int(obj['JumbledWord_Participation'])
    if JumbledWord_Participation>1:
        Success='Y' 
    return [timeStamp,JumbledWord_InitiatedByUser_ID,JumbledWord_Participation,Success]

# READING FROM DynamoDB
yesterday=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data('TB_JumbledWord_Engagement','Date',yesterday)
sheetData=list(map(refactor,sheetData))

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('JWB_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet5 done, successfully')
