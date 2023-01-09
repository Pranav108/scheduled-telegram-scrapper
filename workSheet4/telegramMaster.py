import sys
sys.path.append('..')
from pyrogram import Client
import config
import datetime
import gspread
import json
app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
TARGET='jobcoach_kannada'
todayDate = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
memberList=[]
messageList=[]
userSet=set()
personCount=WCBinitatedCount=0
rowData=[0,0,0,0,'MSG',0,0,'MSG',0,0,'NIL']
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
            # print(message)
            if(message.date.date()==todayDate):
                continue
            if(message.date.date()<yesterday):
                break
            message=json.loads(str(message))
            if('text' in message):
                if(('from_user' in message) and message['from_user'].get('username')=="on9wordchainbot" and ('Turn order:' in message['text'])):
                   WCBinitatedCount=WCBinitatedCount+1
                if 'from_user' in message:
                    userSet.add(message['from_user'].get('id'))
                messageList.append(message)

# Column for OFFLINE and ONLINE can also be add
app.run(main())
rowData[4]=len(userSet)
rowData[5]=len(messageList)
rowData[6]=WCBinitatedCount
rowData[8]=messageList[len(messageList)-1].get('date')
rowData[9]=messageList[0].get('date')
rowData.append(personCount)
rowData.insert(0,yesterday.strftime("%x"))

print(len(messageList))

# PUSHING to JSON
# with open('telegramMaster.json', "w") as file:
#     json.dump(rowData, file)

# PUSHING to SHEET
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
worksheet = sh.get_worksheet(4)
worksheet.append_row(rowData)
