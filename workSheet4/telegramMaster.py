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
personCount=WCBinitatedCount=JWB_initiatedCount=0
rowData=[0,0,0,0,'MSG',0,0,'MSG',0,0,'NIL']
async def main():
    async with app:
        async for member in app.get_chat_members(TARGET):
            member=json.loads(str(member))
            global personCount,WCBinitatedCount,JWB_initiatedCount
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
            if('text' in message):
                if(('from_user' in message) and message['from_user'].get('username')=="on9wordchainbot" and ('Turn order:' in message['text'])):
                   WCBinitatedCount=WCBinitatedCount+1
                if(('from_user' in message) and message['from_user'].get('username')=="jumble_word_bot" and ('Here is the first word' in message['text'])):
                    JWB_initiatedCount=JWB_initiatedCount+1   
                if 'from_user' in message :
                    userSet.add(message['from_user'].get('id'))
                elif 'sender_chat' in message:
                    userSet.add(message['sender_chat'].get('id'))
                messageList.append(message)

# Column for OFFLINE and ONLINE can also be add
app.run(main())
rowData[4]=len(userSet)
rowData[5]=len(messageList)
rowData[6]=WCBinitatedCount
rowData[7]=JWB_initiatedCount
rowData[8]=messageList[len(messageList)-1].get('date')
rowData[9]=messageList[0].get('date')
rowData.append(personCount)
rowData.insert(0,yesterday.strftime("%x"))

# PUSHING to JSON
# with open('telegramMaster.json', "w") as file:
#     json.dump(rowData, file)

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
    'first_message_time':rowData[9],
    'last_message_time':rowData[10],
    'No_of_people_joining_VC':rowData[11],
    'Total_member_in_group':rowData[12],
}
DB.send_data(dataFormat,'ST_Telegram_Master')
print('Data from Telegram_Master_DB')
# print(DB.read_read('ST_Telegram_Master'))

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.get_worksheet(4)
worksheet.append_row(rowData)
print('scrapping in workSheet4 done, successfully')
