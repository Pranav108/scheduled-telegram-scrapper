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
userList=[]
messageList=[]
wordOfTheDay='loream_ipsum_dolar_sit'
userMap={}
async def main():
    async with app:
        async for message in app.get_chat_history(TARGET): 
            # print(message)
            if(message.date.date()==todayDate):
                continue
            if(message.date.date()<yesterday):
                break
            message=json.loads(str(message))
            if('text' in message):
                # No._WCB_Participated
                if(('from_user' in message) and message['from_user'].get('username')=="on9wordchainbot" and ('Turn order:' in message['text'])):
                    for el in message['entities']:
                        if 'user' in el:
                            user_id=el['user'].get('id')
                            if user_id in userMap:
                                userMap[user_id][5]=userMap[user_id][5]+1
                            else:
                                userMap[user_id]=[yesterday.strftime("%x"),user_id,0,'NOT_AVAILABLE',0,1,0,0,'NOT_AVAILABLE','NOT_AVAILABLE']

                # No._WCB_Initiated
                if '/start' in message['text'] and '@on9wordchainbot' in message['text']:
                    user_id=message['from_user'].get('id')
                    if user_id in userMap:
                        userMap[user_id][4]=userMap[user_id][4]+1
                    else:
                        userMap[user_id]=[yesterday.strftime("%x"),user_id,0,'NOT_AVAILABLE',1,0,0,0,'NOT_AVAILABLE','NOT_AVAILABLE']
                
                # Same logic as above two will be applied for JW bot
                
                # if wordOfTheDay is 'loream_ipsum_dolar_sit':
                #      write logic to get word of the day
                # else:
                #     write logic to find if user userd wordOfTheDay
                
                # MessageCount
                user_id=0
                if 'from_user' in message:
                    user_id=message['from_user'].get('id')
                elif 'sender_chat' in message:
                    print
                    user_id=message['sender_chat'].get('id')
                if user_id in userMap:
                    userMap[user_id][2]=userMap[user_id][2]+1
                else:
                    userMap[user_id]=[yesterday.strftime("%x"),user_id,1,'NOT_AVAILABLE',0,0,0,0,'NOT_AVAILABLE','NOT_AVAILABLE']
                
            # messageList.append(message)
            

app.run(main())

userList=list(userMap.values())
print(len(userList))

# PUSHING to JSON
# with open('userData.json', "w") as file:
#     json.dump(userList, file)

# PUSHING to SHEET
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
worksheet = sh.get_worksheet(3)
worksheet.append_rows(userList)

# {
#     user_id = [userid,...............]
#     user_id = [userid,...............]
#     user_id = [userid,...............]
# }
