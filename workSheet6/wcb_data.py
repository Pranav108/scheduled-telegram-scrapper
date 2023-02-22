import sys,os
from pathlib import Path
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
group_chat_id=os.getenv('GROUP_CHAT_ID')
yesterday = datetime.date.today() - datetime.timedelta(days=1)
messageList=[]
sheetData=[]
userMasterData={}
with open('workSheet2/userMaster.json') as f:
   userMasterData = json.load(f)

async def main():
    async with app:
        async for message in app.get_chat_history(group_chat_id):
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
            if 'text' in message and message['text'].startswith('/start') and message['text'].endswith("@on9wordchainbot"):
                messageList.append(message)
            if message[typeOfUser].get('username')=='on9wordchainbot' and 'text' in message and ('Not enough players.' in message['text'] or 'Turn order:' in message['text'] ):
                messageList.append(message)
        
        i=0
        messageListLength=len(messageList)
        messageList.reverse()
        while i<messageListLength:
            typeOfOuterUser=''
            if 'from_user' in messageList[i]:
                typeOfOuterUser='from_user'
            else:
                typeOfOuterUser='sender_chat'
            outerMessageText = messageList[i].get('text')
            outerUser_ID = str(messageList[i][typeOfOuterUser].get('id'))
            outerMsgDate = messageList[i].get('date')
            if outerMessageText.startswith('/start') and outerMessageText.endswith("@on9wordchainbot"):
                tempCounter=i+1
                while(tempCounter<messageListLength):
                    msgObj=messageList[tempCounter]
                    typeOfUser=''
                    if 'from_user' in msgObj:
                        typeOfUser='from_user'
                    else:
                        typeOfUser='sender_chat'
                    innerMessageText = msgObj.get('text')
                    innerUser_ID=str(msgObj[typeOfUser].get('id'))
                    innerMsgDate=msgObj['date']
                    InitiatedByUserName='NOT_FOUND'
                    if innerMessageText.startswith('/start') and innerMessageText.endswith("@on9wordchainbot"):
                        if innerUser_ID in userMasterData:
                            InitiatedByUserName=userMasterData[innerUser_ID][0]
                        sheetData.append([innerMsgDate,innerUser_ID,InitiatedByUserName,0,'N'])
                    elif 'Not enough players.' in innerMessageText:
                        if outerUser_ID in userMasterData:
                            InitiatedByUserName=userMasterData[outerUser_ID][0]
                        sheetData.append([outerMsgDate,outerUser_ID,InitiatedByUserName,1,'N'])
                        break
                    elif 'Turn order:' in innerMessageText:
                        playerCount=len(msgObj['entities'])-1
                        if outerUser_ID in userMasterData:
                            InitiatedByUserName=userMasterData[outerUser_ID][0]
                        sheetData.append([outerMsgDate,outerUser_ID,InitiatedByUserName,playerCount,'Y'])
                        break
                    else:
                        print('SOMETHING WIERD!!')
                        break
                    tempCounter=tempCounter+1
                i=tempCounter+1                    
            else:
                i=i+1
                            
app.run(main())

# PUSHING to DynamoDB
for el in sheetData:
    print(el)
    dataFormat={
        'Datetime':el[0],
        'WordChainBot_InitiatedByUser_ID':el[1],
        'WordChainBot_InitiatedByUserName':el[2],
        'participantCount':el[3],
        'Success':el[4],
    }
    DB.send_data(dataFormat,'ST_WCB_Data')
print('Data from WCB_Data_DB')
    
# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('WCB_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet6 done, successfully')
