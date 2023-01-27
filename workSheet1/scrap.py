import sys,os
from dotenv import load_dotenv
load_dotenv()
from pyrogram import Client
import datetime
import gspread
import json

app = Client(
    "YOUR_BOT",
    api_id = os.getenv('API_ID'),
    api_hash = os.getenv('API_HASH')
)
todayDate = datetime.date.today()
yesterday = todayDate - datetime.timedelta(days=1)
TARGET='jobcoach_kannada'
useFull=[0]*24
indexAdder=messageSum=messageCount=botInitiatedCount=0

# SCRAPPING LOGIC
async def scrap():
    async with app:
        async for message in app.get_chat_history(TARGET):
            if(message.date.date()>yesterday):
                continue
            if(message.date.date()<yesterday):
                break
            global messageCount,botInitiatedCount
            message=json.loads(str(message))
            if('text' in message):
                messageTime=message['date'].split(" ")[1]
                messageHour=int(messageTime.split(":")[0])
                useFull[(messageHour+17)%24]=useFull[(messageHour+17)%24]+1
                if(('from_user' in message) and message['from_user'].get('username')=="on9wordchainbot" and (' joined. There are now 2 players.' in message['text'])):
                    botInitiatedCount=botInitiatedCount+1
app.run(scrap())

# REFACTORING LOGIC
for i in range(24):
    messageSum=messageSum+useFull[i+indexAdder]
    if((i+indexAdder)%5==3):
        indexAdder=indexAdder+1
        useFull.insert(i+indexAdder,messageSum)
        messageCount = messageCount + messageSum
        messageSum=0
useFull.insert(0,yesterday.strftime("%x"))
useFull.extend([messageCount,botInitiatedCount])
print('scrappinmg in wordsheet1 done, successfully')
# PUSHING to JSON
# with open('messageList.json', "w") as file:
#     json.dump(messageList, file,indent=4)

# PUSHING LOGIC
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.get_worksheet(1)
worksheet.append_row(useFull)