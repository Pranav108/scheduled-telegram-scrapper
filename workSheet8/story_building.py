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

userMasterData={}
yesterday = datetime.date.today() - datetime.timedelta(days=1)

with open('workSheet2/userMaster.json') as f:
   userMasterData = json.load(f)
   
def refactor(obj):
    timeStamp=obj['timestamp'].split('.')[0].replace('T',' ')
    success='N'
    InitiatedByUser_ID=str(obj['user_id'])
    participation_count=int(obj['n_participants'])
    if participation_count>1:
        success='Y'
    fullName=''
    if InitiatedByUser_ID not in userMasterData:
        print('cannot find user data in UserMaster')
    else:
        fullName=userMasterData[InitiatedByUser_ID][0]
    return [timeStamp,InitiatedByUser_ID,fullName,participation_count,success]

# READING FROM DynamoDB
yesterday=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data('TB_StoryBuilding_Data','date',yesterday)
sheetData=list(map(refactor,sheetData))
sheetData.sort()

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('StoryBuilding_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet8 done, successfully')
