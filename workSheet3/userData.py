import sys,os
from dotenv import load_dotenv
load_dotenv()
import datetime
import json
import time
import gspread
import re
from pyrogram import Client, enums
sys.path.append(os.getcwd())
from db.db_model import DynamoDB_con
DB = DynamoDB_con()

app = Client(
    "YOUR_BOT",
    api_id = os.getenv('API_ID'),
    api_hash = os.getenv('API_HASH')
)
cur_path = os.path.dirname(__file__)
TARGET='jobcoach_kannada'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
userList=[]
messageList_ID=[]
# wordOfTheDay='reality'
userMap={
    -1001636582068:[yesterday.strftime("%x"),-1001636582068,0,'N',0,0,0,0,0,0,'NOT_AVAILABLE','NOT_AVAILABLE']
    }
useFullMessage=[]
jwb_data=[]

def refactor(obj):
    print(obj)
    JumbledWord_InitiatedByUser_ID=int(obj['JumbledWord_InitiatedByUser_ID'])
    participants=obj['participants_ids'][:-1].split(',')
    if JumbledWord_InitiatedByUser_ID in userMap:
        userMap[JumbledWord_InitiatedByUser_ID][6]=userMap[JumbledWord_InitiatedByUser_ID][6]+1
    for el in participants:
        participant=int(el)
        if participant in userMap:
            userMap[participant][7]=userMap[participant][7]+1
    return 0

def checkValid(i, arr):
    user_id=0
    while i < len(arr) :
        txt=arr[i]['text']
        if '/start' in txt and '@on9wordchainbot' in txt:
            if 'from_user' in arr[i]:
                user_id=int(arr[i]['from_user'].get('id'))
            else :
                user_id=int(arr[i]['sender_chat'].get('id'))
            break
        i=i+1
    while i < len(arr) :
        txt=arr[i]['text']
        if 'There are now 2 players.' in txt:
            return i+1,True,user_id
        if 'Not enough players.' in txt:
            return i+1,False,user_id
        i=i+1
    return len(arr)+1,False,0   
        
async def findWod():
    async with app:
        async for message in app.search_messages(chat_id=TARGET,query='Word of the day' ,filter=enums.MessagesFilter.ANIMATION,limit=1):
            message=json.loads(str(message))
            global wordOfTheDay
            messageTxt = message.get('caption')
            result = re.search('- (.*):', messageTxt)
            if result:
                wordOfTheDay=result.group(1).casefold()
            print(wordOfTheDay)

async def main():
    async with app:
        async for member in app.get_chat_members(TARGET):
            member=json.loads(str(member))
            userID=member['user'].get('id')                
            messageList_ID.append(userID)
        for id in messageList_ID:
            userMap[id]=[yesterday.strftime("%x"),id,0,'N',0,0,0,0,0,0,'NOT_AVAILABLE','NOT_AVAILABLE']
        
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
            if ('text' in message or 'caption' in message):
                user_id=message[typeOfUser].get('id')
                user_name=message[typeOfUser].get('username')
                global wordOfTheDay
                
                # No._WCB_Participated
                if user_name=="on9wordchainbot" :
                    if 'Turn order:' in message['text']:
                        for el in message['entities']:
                            if  el["type"] == "MessageEntityType.TEXT_MENTION" and 'user' in el:
                                mentionedId = el['user'].get('id')
                                if mentionedId in userMap:
                                    userMap[mentionedId][5]=userMap[mentionedId][5]+1
                    if 'Not enough players.' in message['text'] or 'There are now 2 players.' in message['text'] :
                        useFullMessage.append(message)

                # No._WCB_Initiated
                if 'text' in message and '/start' in message['text'] and '@on9wordchainbot' in message['text']:
                    useFullMessage.append(message)

                # MessageCount
                if user_id in userMap:
                    userMap[user_id][2]=userMap[user_id][2]+1
                if wordOfTheDay != 'NO_WORD_YET':
                    targetMessage=''
                    if 'caption' in message:
                        targetMessage=message.get('caption').casefold()
                    if 'text' in message:
                        targetMessage=message.get('text').casefold()
                    if wordOfTheDay in targetMessage:
                        userMap[user_id][3]='Y'
        
        i=0
        useFullMessage.reverse()
        while i<len(useFullMessage):
            i,result,user_id=checkValid(i,useFullMessage)
            if result:
                userMap[user_id][4]=userMap[user_id][4]+1
         
        # to get JWB data
        yesterday_str=yesterday.strftime('%Y-%m-%d')
        jwb_data=DB.read_data('TB_JumbledWord_Engagement','Date',yesterday_str)
        for el in jwb_data:
            refactor(el)
        
app.run(findWod())
app.run(main())

userList=list(userMap.values())

# PUSHING to JSON
# with open(os.path.join(cur_path, 'userData.json'), "w") as file:
#     json.dump(userList, file,indent=4)
    
# PUSHING to DynamoDB
for el in userList:
    dataFormat={
        'ID':str(time.time()*1000),
        'Date':el[0],
        'User_ID':el[1],
        'No_of_message_sent':el[2],
        'used_WOD':el[3],
        'No._WCB_Initiated':el[4],
        'No._WCB_Participated':el[5],
        'No._JWB_Initiated':el[6],
        'No._JWB_Participated':el[7],
        'No._QuizQues_Attempted':el[8],
        'No._QuizQues_Correct':el[9],
    }
    DB.send_data(dataFormat,'ST_User_Data')
print('Data from User_Data_DB')

# # PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.get_worksheet(4)
worksheet.append_rows(userList)
print('scrapping in workSheet3 done, successfully')
