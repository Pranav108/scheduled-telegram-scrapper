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
            if 'text' in message and '/start' in message['text'] and '@on9wordchainbot' in message['text']:
                messageList.append(message)
            if message[typeOfUser].get('username')=='on9wordchainbot' and 'text' in message and ('Not enough players.' in message['text'] or 'Turn order:' in message['text'] ):
                messageList.append(message)
        
        i=0
        messageListLength=len(messageList)
        messageList.reverse()
        while i<messageListLength:
            messageText = messageList[i].get('text')
            if '/start' in messageText and '@on9wordchainbot' in messageText:
                tempCounter=i+1
                while(tempCounter<messageListLength):
                    msgObj=messageList[tempCounter]
                    if 'from_user' in msgObj:
                        typeOfUser='from_user'
                    else:
                        typeOfUser='sender_chat'
                    messageText = msgObj.get('text')
                    userID=msgObj[typeOfUser].get('id')
                    msgDate=msgObj['date']
                    if '/start' in messageText and '@on9wordchainbot' in messageText:
                        sheetData.append([msgDate,userID,0,'N'])
                    elif 'Not enough players.' in messageText:
                        sheetData.append([msgDate,userID,1,'N'])
                        break
                    elif 'Turn order:' in messageText:
                        playerCount=len(msgObj['entities'])-1
                        sheetData.append([msgDate,userID,playerCount,'Y'])
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
print(sheetData)
for el in sheetData:
    print(el)
    dataFormat={
        'Datetime':el[0],
        'WordChainBot_InitiatedByUser_ID':el[1],
        'participantCount':el[2],
        'Success':el[3],
    }
    DB.send_data(dataFormat,'ST_WCB_Data')
print('Data from WCB_Data_DB')
    
# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('WCB_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet6 done, successfully')
