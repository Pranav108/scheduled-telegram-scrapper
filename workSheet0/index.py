import sys
sys.path.append('..')
from pyrogram import Client
import config
import datetime
import json
app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
TARGET='jobcoach_kannada'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
messageList=[]
async def main():
    async with app:
        async for message in app.get_chat_history(TARGET):
            if(message.date.date()<yesterday):
                break
            messageList.append(json.loads(str(message)))

app.run(main())

# print(messageList)
print(len(messageList))
with open('singleDayData.json', "w") as file:
    json.dump(messageList, file)


