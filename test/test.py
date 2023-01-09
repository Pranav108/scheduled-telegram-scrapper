import sys
sys.path.append('..')
from pyrogram import Client
import config
import datetime
import json
import re
app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
TARGET='pranav_test_grp'
# TARGET='jobcoach_kannada'
lat=25.427429176859505
lon=81.7955244472255
todayDate = datetime.date.today()
messageList=[]
wordOfTheDay=''
async def scrap():
    async with app:
        async for message in app.get_chat_history(TARGET,limit=1): 
        # message = await app.get_nearby_chats(latitude=lat, longitude=lon)
        # print(chats)
            # print(message)
            message=json.loads(str(message))
            if 'text' in message and 'sender_chat' not in message:
                global wordOfTheDay    
                
                if wordOfTheDay :
                    if wordOfTheDay in message['text']:
                        print('have WOD')
                        
                elif 'Word of the da' in message['text']:
                    print('dont have WOD, assign')
                    print(message['text'])
                    m = re.search('_(.+?)_', message.get('text'))
                    if m:
                        wordOfTheDay=m.group(1)
app.run(scrap())

# print(len(messageList))

# # PUSHING to JSON
# with open('test.json', "w") as file:
#     json.dump(messageList, file)

