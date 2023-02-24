import sys,os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import datetime
import gspread
import json
sys.path.append(os.getcwd())
from config import * 
from db.db_model import DynamoDB_con
DB = DynamoDB_con()

userMasterData={}
yesterday = datetime.date.today() - datetime.timedelta(days=1)

def refactored_obj(obj):
    fullName=obj['Full_Name']
    userName=obj['User_Name']
    dateOfJoining=obj['Date_of_Joining']
    dateOfLeaving=obj['Date_of_Leaving']
    lastSeen=obj['Last_Seen']
    lastActivity=obj['Last_Activity']
    return [fullName,userName,dateOfJoining,dateOfLeaving,lastSeen,lastActivity]

sheetData=DB.read_all_data(user_master)
for el in sheetData:
    userMasterData[str(el['User_ID'])]=refactored_obj(el)
   
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
    return [timeStamp,int(InitiatedByUser_ID),fullName,participation_count,success]

# READING FROM DynamoDB
yesterday=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data(storybuilding_data,'date',yesterday)
sheetData=list(map(refactor,sheetData))
sheetData.sort()

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('StoryBuilding_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet8 done, successfully')
