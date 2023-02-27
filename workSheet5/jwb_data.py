import sys,os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import datetime
import gspread
import json
sys.path.append(os.getcwd())
from config import * 

yesterday = datetime.date.today() - datetime.timedelta(days=1)
userMasterData={}

sheetData=DB.read_all_data(user_master)
for el in sheetData:
    userMasterData[str(el['User_ID'])]=el['Full_Name']

def refactor(obj):
    timeStamp=obj['Datetime'].split('.')[0]
    Success='N'
    JumbledWord_InitiatedByUser_ID=str(obj['JumbledWord_InitiatedByUser_ID'])
    JumbledWord_Participation=int(obj['JumbledWord_Participation'])
    if JumbledWord_Participation>1:
        Success='Y' 
    fullName='NOT_FOUND'
    if JumbledWord_InitiatedByUser_ID in userMasterData:
        fullName=userMasterData[JumbledWord_InitiatedByUser_ID]
    return [timeStamp,int(JumbledWord_InitiatedByUser_ID),fullName,JumbledWord_Participation,Success]

# READING FROM DynamoDB
yesterday=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data(jumbledword_engagement,'Date',yesterday)
sheetData=list(map(refactor,sheetData))

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('JWB_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet5 done, successfully')
