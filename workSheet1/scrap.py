import sys
sys.path.append('..')
from pyrogram import Client
import datetime
import gspread
import json
import config

app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
todayDate = datetime.date.today()
yesterday = todayDate - datetime.timedelta(days=3)
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

# PUSHING LOGIC
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
worksheet = sh.get_worksheet(1)
worksheet.append_row(useFull)