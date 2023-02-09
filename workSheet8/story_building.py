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
# for push in sheet
def refactor(obj):
    timeStamp=obj['timeStamp'].split('.')[0].replace('T',' ')
    success='N'
    InitiatedByUser_ID=str(obj['initiated_by'])
    participation_count=int(obj['participation_count'])
    if participation_count>1:
        success='Y'
    fullName=''
    if InitiatedByUser_ID not in userMasterData:
        print('cannot find user data in UserMaster')
    else:
        fullName=userMasterData[InitiatedByUser_ID][0]
    return [timeStamp,InitiatedByUser_ID,fullName,participation_count,success]

#for push in my DB table 
# def refactor(obj):
#     timeStamp=obj['timestamp'],
#     InitiatedByUser_ID=str(obj['user_id'])
#     participation_count=int(obj['n_participants'])
#     return [''.join(timeStamp),InitiatedByUser_ID,participation_count]

# READING FROM DynamoDB
yesterday=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data('ST_StoryBuilding_Data','Date',yesterday)
# sheetData=DB.read_data('TB_StoryBuilding_Data',yesterday)
sheetData=list(map(refactor,sheetData))

with open('workSheet8/DB_data.json', "w") as file:
    json.dump(sheetData, file,indent=4)

# PushIng to DynamoDB(FOR TESTING ONLY)
# for el in sheetData:
#     obj={
#         'Date':el[0].split('.')[0].split('T')[0],
#         'timeStamp':el[0],
#         'initiated_by':el[1],
#         'participation_count':el[2]
#     }
#     DB.send_data(obj,'ST_StoryBuilding_Data')
# print('Data from StoryBuilding_DB')

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.get_worksheet(9)
worksheet.append_rows(sheetData)
print('scrapping in workSheet8 done, successfully')
