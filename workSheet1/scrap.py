import sys,os
from dotenv import load_dotenv
load_dotenv()
import datetime
import gspread
import json
sys.path.append(os.getcwd())
from config import * 

todayDate = datetime.date.today()
yesterday = todayDate - datetime.timedelta(days=1)
group_chat_id=os.getenv('GROUP_CHAT_ID')
useFull=[0]*24
indexAdder=messageSum=messageCount=botInitiatedCount=0

# SCRAPPING LOGIC
async def scrap():
    async with app:
        async for message in app.get_chat_history(group_chat_id):
            if(message.date.date()>yesterday):
                continue
            if(message.date.date()<yesterday):
                break
            global messageCount,botInitiatedCount
            message=json.loads(str(message))
            if('text' in message or 'caption' in message):
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
# PUSHING to JSON
# with open('messageList.json', "w") as file:
#     json.dump(messageList, file,indent=4)

dataFormat={
    'Timing':useFull[0],
    '07:00 - 07:59':useFull[1],
    '08:00 - 08:59':useFull[2],
    '09:00 - 09:59':useFull[3],
    '10:00 - 10:59':useFull[4],
    'Total_Message':useFull[5],
    '11:00 - 11:59':useFull[6],
    '12:00 - 12:59':useFull[7],
    '13:00 - 13:59':useFull[8],
    '14:00 - 14:59':useFull[9],
    'Total_Message':useFull[10],
    '15:00 - 15:59':useFull[11],
    '16:00 - 16:59':useFull[12],
    '17:00 - 17:59':useFull[13],
    '18:00 - 18:59':useFull[14],
    'Total_Message':useFull[15],
    '19:00 - 19:59':useFull[16],
    '20:00 - 20:59':useFull[17],
    '21:00 - 21:59':useFull[18],
    '22:00 - 22:59':useFull[19],
    'Total_Message':useFull[20],
    '23:00 - 23:59':useFull[21],
    '00:00 - 00:59':useFull[22],
    '01:00 - 01:59':useFull[23],
    '02:00 - 02:59':useFull[24],
    'Total_Message':useFull[25],
    '03:00 - 03:59':useFull[26],
    '04:00 - 04:59':useFull[27],
    '05:00 - 05:59':useFull[28],
    '06:00 - 06:59':useFull[29],
    'Total_Message':useFull[30],
    'Total_Message_In_Day':useFull[31],
    'WCB_initiated_count_per_day':useFull[32]
}
DB.send_data(dataFormat,content_analysis)
print(f"Data from {content_analysis}")

# PUSHING LOGIC
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet("Content_Analysis")
worksheet.append_row(useFull)
print('scrapping in workSheet1 done, successfully')