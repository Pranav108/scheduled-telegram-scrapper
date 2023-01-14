import sys
sys.path.append('..')
from pyrogram import enums
from pyrogram import Client
import config
import datetime
import gspread
import json
import re
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
wordOfTheDay='NO_WORD_YET'
userMap={}

async def findWod():
    async with app:
        async for message in app.search_messages(chat_id=TARGET,query='Word of the day' ,filter=enums.MessagesFilter.ANIMATION,limit=1):
            message=json.loads(str(message))
            global wordOfTheDay
            messageTxt = message.get('caption')
            result = re.search('- (.*):', messageTxt)
            if result:
                wordOfTheDay=result.group(1).casefold()

async def main():
    async with app:
        async for member in app.get_chat_members(TARGET):
            member=json.loads(str(member))
            messageList.append(member['user'].get('id'))
            for id in messageList:
                userMap[id]=[yesterday.strftime("%x"),id,0,'N',0,0,0,0,'NOT_AVAILABLE','NOT_AVAILABLE']
        
        async for message in app.get_chat_history(TARGET): 
            if(message.date.date()>yesterday):
                continue
            if(message.date.date()<yesterday):
                break
            message=json.loads(str(message))
            if 'text' in message and 'sender_chat' not in message:
                user_id=message['from_user'].get('id')
                global wordOfTheDay
                
                # No._WCB_Participated
                if(('from_user' in message) and message['from_user'].get('username')=="on9wordchainbot" and ('Turn order:' in message['text'])):
                    for el in message['entities']:
                        if  el["type"] == "MessageEntityType.TEXT_MENTION" and 'user' in el:
                            mentionedId = el['user'].get('id')
                            userMap[mentionedId][5]=userMap[mentionedId][5]+1

                # No._WCB_Initiated
                if '/start' in message['text'] and '@on9wordchainbot' in message['text']:
                    userMap[user_id][4]=userMap[user_id][4]+1
                
                # Same logic as above two will be applied for JW bot
                
                # if wordOfTheDay is 'loream_ipsum_dolar_sit':
                #      write logic to get word of the day
                # else:
                #     write logic to find if user userd wordOfTheDay
                
                # MessageCount
                userMap[user_id][2]=userMap[user_id][2]+1
                if wordOfTheDay != 'NO_WORD_YET':
                    if wordOfTheDay in message['text'].casefold():
                        userMap[user_id][3]='Y'
                
app.run(findWod())
app.run(main())

userList=list(userMap.values())

# PUSHING to JSON
with open('userData.json', "w") as file:
    json.dump(userList, file)

# PUSHING to SHEET
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1uO7meUfKpn-qUYpOVhwofc1jW24Gmv0iNrkqw5OxgLk')
worksheet = sh.get_worksheet(3)
worksheet.append_rows(userList)

