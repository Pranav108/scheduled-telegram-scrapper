import sys,os
from dotenv import load_dotenv
load_dotenv()
import datetime
import json
import time
import gspread
import re
sys.path.append(os.getcwd())
from pyrogram import enums
from config import * 

cur_path = os.path.dirname(__file__)
group_chat_id=os.getenv('GROUP_CHAT_ID')
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday_str=yesterday.strftime('%Y-%m-%d')
userList=[]
messageList_ID=[]
useFullMessage=[]
jwb_data=[]
quiz_number=0
wordOfTheDay='NO_WORD_YET'
userMap={
    -1001636582068:[yesterday_str,-1001636582068,0,'N',0,0,0,0,0,0,0,0]
    }
   
def refactor_JWB(obj):
    JumbledWord_InitiatedByUser_ID=int(obj['JumbledWord_InitiatedByUser_ID'])
    participants=obj['participants_ids'][:-1].split(',')
    if JumbledWord_InitiatedByUser_ID in userMap:
        userMap[JumbledWord_InitiatedByUser_ID][6]=userMap[JumbledWord_InitiatedByUser_ID][6]+1
    for el in participants:
        participant=int(el)
        if participant in userMap:
            userMap[participant][7]=userMap[participant][7]+1

def refactor_SBB(obj):
    SBB_InitiatedByUser_ID=int(obj['user_id'])
    participants=obj['participants'].split(',')
    if SBB_InitiatedByUser_ID in userMap:
        userMap[SBB_InitiatedByUser_ID][8]=userMap[SBB_InitiatedByUser_ID][8]+1
    for el in participants:
        participant=int(el)
        if participant in userMap:
            userMap[participant][9]=userMap[participant][9]+1

def refactor_quizSession(obj):
    user_id=int(obj['user_id'])
    scores=obj['scores']
    QuizQues_Attempted=QuizQues_Correct=0
    for el in scores:
        if el is not None:
            QuizQues_Attempted=QuizQues_Attempted+1
            if el == 1:
                QuizQues_Correct=QuizQues_Correct+1
    if user_id in userMap:
        userMap[user_id][10]=QuizQues_Attempted
        userMap[user_id][11]=QuizQues_Correct
    else:
        print('cannot find user-data for quiz session')
            
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
        async for message in app.search_messages(chat_id=group_chat_id,query='Word of the day' ,filter=enums.MessagesFilter.ANIMATION,limit=1):
            message=json.loads(str(message))
            global wordOfTheDay
            messageTxt = message.get('caption')
            result = re.search('- (.*):', messageTxt)
            if result:
                wordOfTheDay=result.group(1).casefold()
            print(wordOfTheDay)

async def main():
    async with app:
        global yesterday_str
        async for member in app.get_chat_members(group_chat_id):
            member=json.loads(str(member))
            userID=member['user'].get('id')                
            messageList_ID.append(userID)
        for id in messageList_ID:
            userMap[id]=[yesterday_str,id,0,'N',0,0,0,0,0,0,0,0]
        
        async for message in app.get_chat_history(group_chat_id): 
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
            if result and user_id in userMap:
                userMap[user_id][4]=userMap[user_id][4]+1
         
        # to get JWB data
        yesterday_str=yesterday.strftime('%Y-%m-%d')
        jwb_data=DB.read_data(jumbledword_engagement,'Date',yesterday_str)
        for el in jwb_data:
            refactor_JWB(el)
            
        # to get StoryBuilding data
        sbb_data=DB.read_data(storybuilding_data,'date',yesterday_str)
        for el in sbb_data:
            refactor_SBB(el)
        
        # to get quizBot session
        quizSession_data=DB.read_data(quizbot_session,'date',yesterday_str)
        for el in quizSession_data:
            refactor_quizSession(el)
        
app.run(findWod())
app.run(main())

userList=list(userMap.values())
        
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
        'No._SBB_Initiated':el[8],
        'No._SBB_Participated':el[9],
        'No._QuizQues_Attempted':el[10],
        'No._QuizQues_Correct':el[11],
    }
    DB.send_data(dataFormat,user_data)
print(f"Data from {user_data}")

# # PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('User_Data')
worksheet.append_rows(userList)
print('scrapping in workSheet3 done, successfully')
