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
yesterday = datetime.date.today() - datetime.timedelta(days=1)
messageList=[]
sheetData=[]
async def main():
    async with app:
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

# PUSHING to JSON
# with open('messageList.json', "w") as file:
#     json.dump(messageList, file)

# PUSHING to SHEET
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
worksheet = sh.get_worksheet(6)
worksheet.append_rows(sheetData)
