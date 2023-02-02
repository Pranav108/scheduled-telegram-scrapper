import sys,os
from dotenv import load_dotenv
load_dotenv()
from pyrogram import Client
import datetime
import json
sys.path.append(os.getcwd())
from db.db_model import DynamoDB_con
DB = DynamoDB_con()
import gspread

cur_path = os.path.dirname(__file__)
app = Client(
    "YOUR_BOT",
    api_id = os.getenv('API_ID'),
    api_hash = os.getenv('API_HASH')
)
TARGET='jobcoach_kannada'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
userMap={}
activityList=[]
with open(os.path.join(cur_path, 'userMaster.json')) as f:
   userMap = json.load(f)
    
async def getUserInfo(user,Date_of_Joining=None,Date_of_Leaving=None):
    User_ID=user.get('id','NOT_AVL')
    User_Name=user.get('username','NOT_AVL')
    Full_Name=user.get('first_name','')+' '+user.get('last_name','')
    Last_Message='NOT_FOUND'
    if Date_of_Joining is None:
        Date_of_Joining='NOT_AVL'
    else:
        Last_Message='NO_ACTIVITY'
    if Date_of_Leaving is None:
        Date_of_Leaving='NOT_AVL'
    Last_Seen=user.get('status','A.NOT_AVILABLE').split('.')[1]
    return [Full_Name,User_Name,Date_of_Joining,Date_of_Leaving,Last_Seen,Last_Message]

def makeList(userMap):
    ans=[]
    for key in userMap:
        temp=userMap[key]
        temp.insert(0,key)
        ans.append(temp)
    return ans

async def scrap(activityList):        
    for event in reversed(activityList):
        action=event.get('action').split('.')[1]
        if action=='MEMBER_JOINED':
            id=str(event['user'].get('id'))
            updateUser=await getUserInfo(user=event.get('user'),Date_of_Joining=event.get('date').split(' ')[0])
            if id in userMap.keys():
                del userMap[id]
            userMap[id]=updateUser    
        elif action=='MEMBER_LEFT':
            id=str(event['user'].get('id'))
            Date_of_Joining=None
            if id in userMap.keys():
                Date_of_Joining=userMap[id][2]
            updateUser=await getUserInfo(user=event.get('user'),Date_of_Joining=Date_of_Joining,Date_of_Leaving=event.get('date').split(' ')[0])             
            if id in userMap.keys():
                del userMap[id]
            userMap[id]=updateUser
        elif action=='USERNAME_CHANGED':
            id=str(event['user'].get('id'))
            if id in userMap.keys():
                Date_of_Joining=userMap[id][2]
                Date_of_Leaving=userMap[id][3]
            updateUser=await getUserInfo(user=event.get('user'),Date_of_Joining=Date_of_Joining,Date_of_Leaving=Date_of_Leaving)             
            userMap[id]=updateUser
            
                
async def makeActivityList():
    async with app:
        async for event in app.get_chat_event_log(TARGET):
            if(event.date.date()>yesterday):
                continue
            if(event.date.date()<yesterday):
                break
            event=json.loads(str(event))
            action=event.get('action').split('.')[1]
            if action=='MEMBER_JOINED' or action=='MEMBER_LEFT' or action=='USERNAME_CHANGED':
                activityList.append(event)
            
        await scrap(activityList)
        async for message in app.get_chat_history(TARGET):
            if(message.date.date()>yesterday):
                continue
            if(message.date.date()<yesterday):
                break
            message=json.loads(str(message))
            user={}
            if 'from_user' in message:
                user=message['from_user']
            elif 'sender_chat' in message:
                user=message['sender_chat']
            else:
                print(message)
            userID=str(user.get('id'))
            if userID in userMap:
                userMap[userID][4]='TODAY'
                userMap[userID][5]=message['date'].split(' ')[0]
                            
app.run(makeActivityList())

# PUSHING to JSON
with open(os.path.join(cur_path, 'userMaster.json'), "w") as file:
    json.dump(userMap, file,indent=4)

result=makeList(userMap)

# PUSHING to DynamoDB
# DB.deleteTotalData('ST_User_Master')
# for el in result:
#     dataFormat={
#         'User_ID':el[0],
#         'FirstName_LastName':el[1],
#         'User_Name':el[2],
#         'Date_of_Joining':el[3],
#         'No.Date of Leaving':el[4],
#         'Last_Seen':el[5],
#         'Last Activity':el[6],
#     }
#     DB.send_data(dataFormat,'ST_User_Master')
# print('Data from User_Master_DB')

# PUSHING to SHEET
result.insert(0,['User_ID','FirstName+LastName','User_Name','Date of Joining',	'Date of Leaving','	Last Seen',	'Last Activity'])
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.get_worksheet(2)
worksheet.clear()
worksheet.append_rows(result)
print('scrapping in workSheet2 done, successfully')
