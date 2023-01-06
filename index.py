from pyrogram import Client
import pyrogram
import datetime
import json
app = Client(
    "YOUR_BOT",
    api_id='29216885',
    api_hash='99edbf3555814eede3496f758c30ec3c',
)
yesterday = datetime.date.today() - datetime.timedelta(days=1)
TARGET='jobcoach_kannada'
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


