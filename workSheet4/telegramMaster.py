import sys,os
from dotenv import load_dotenv
load_dotenv()
from pyrogram import Client
import datetime
import gspread

import json
sys.path.append(os.getcwd())
from db.db_model import DynamoDB_con
DB = DynamoDB_con()
app = Client(
    "YOUR_BOT",
    api_id = os.getenv('API_ID'),
    api_hash = os.getenv('API_HASH')
)
TARGET='jobcoach_kannada'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
memberList=[]
messageList=[]
userSet=set()
personCount=WCBinitatedCount=JWB_initiatedCount=SBB_initiatedCount=0
rowData=[0,0,0,0,0,0,0,0,0,0,0,'NIL']
async def main():
    async with app:
        async for member in app.get_chat_members(TARGET):
            member=json.loads(str(member))
            global personCount,WCBinitatedCount
            if 'status' in member['user']:
                personCount=personCount+1
                status=member['user'].get('status').split('.')[1]
                if status == 'RECENTLY' :
                    rowData[0]=rowData[0]+1
                if status == 'LAST_WEEK':
                    rowData[1]=rowData[1]+1
                if status == 'LAST_MONTH':
                    rowData[2]=rowData[2]+1
                if status == 'LONG_AGO':
                    rowData[3]=rowData[3]+1
            memberList.append(member)
            
        async for message in app.get_chat_history(TARGET): 
            if(message.date.date()>yesterday):
                continue
            if(message.date.date()<yesterday):
                break
            message=json.loads(str(message))
            typeOfUser=''
            if 'from_user' in message:
                typeOfUser='from_user'
            else:
                typeOfUser='sender_chat'
            if('text' in message):
                if(message[typeOfUser].get('username')=="on9wordchainbot" and ('Turn order:' in message['text'])):
                   WCBinitatedCount=WCBinitatedCount+1
                userSet.add(message[typeOfUser].get('id'))
                messageList.append(message)
            if 'caption' in message:
                userSet.add(message[typeOfUser].get('id'))
                messageList.append(message)
        global JWB_initiatedCount,SBB_initiatedCount
        yesterday_str=yesterday.strftime('%Y-%m-%d')
        # to get JumbledWordBot data
        jwb_data=DB.read_data('TB_JumbledWord_Engagement','Date',yesterday_str)
        for el in jwb_data:
            participants_count=int(el['JumbledWord_Participation'])
            if participants_count>1:
                JWB_initiatedCount=JWB_initiatedCount+1
            
        # to get StoryBuilding data
        sbb_data=DB.read_data('TB_StoryBuilding_Data','date',yesterday_str)
        for el in sbb_data:
            participants_count=int(el['n_participants'])
            if participants_count>1:
                SBB_initiatedCount=SBB_initiatedCount+1

app.run(main())
rowData[4]=len(userSet)
rowData[5]=len(messageList)
rowData[6]=WCBinitatedCount
rowData[7]=JWB_initiatedCount
rowData[8]=SBB_initiatedCount
rowData[9]=messageList[len(messageList)-1].get('date')
rowData[10]=messageList[0].get('date')
rowData.append(personCount)
rowData.insert(0,yesterday.strftime("%x"))

# PUSHING to DynamoDB
dataFormat={
    'Date':rowData[0],
    'last_seen_recently':rowData[1],
    'last_seen_a_week_ago':rowData[2],
    'last_seen_a_month_ago':rowData[3],
    'last_seen_a_long_time_ago ':rowData[4],
    'active_on_group':rowData[5],
    'Total_messages':rowData[6],
    'WCB_initiated':rowData[7],
    'JWB_initiated':rowData[8],
    'SBB_initiated':rowData[9],
    'first_message_time':rowData[10],
    'last_message_time':rowData[11],
    'Total_member_in_group':rowData[13],
}
DB.send_data(dataFormat,'ST_Telegram_Master')
print('Data from Telegram_Master_DB')

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('Telegram_Master')
worksheet.append_row(rowData)
print('scrapping in workSheet4 done, successfully')
