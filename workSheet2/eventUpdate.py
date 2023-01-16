import sys
sys.path.append('..')
from pyrogram import Client
import config
import datetime
import json
import gspread
app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
TARGET='jobcoach_kannada'
todayDate = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
tempUserMap={}
userMap={}
userMap2={}
activityList=[]
with open('userMaster.json') as f:
   userMap = json.load(f)
   
def getLastSeen(user):
    Last_Seen=user.get('status','A.NOT_AVILABLE').split('.')[1]
    if 'last_online_date' in user:
        last_online_date=user.get('last_online_date').split(' ')[0]
        Last_Seen_Date=datetime.datetime.strptime(last_online_date, "%Y-%m-%d").date()
        if Last_Seen_Date>=yesterday:
            Last_Seen='TODAY'
    return Last_Seen
            
async def getLastActivity(user_id):
    Last_Message='NO_ACTIVITY'
    async for lastMessage in app.search_messages(TARGET, limit=1,from_user=user_id):
        lastMessage=json.loads(str(lastMessage))
        if lastMessage:
            Last_Message = lastMessage['date'].split(' ')[0]
    return Last_Message
    
async def getUserInfo(user,Date_of_Joining=None,Date_of_Leaving=None):
    User_ID=user.get('id','NOT_AVL')
    User_Name=user.get('username','NOT_AVL')
    Full_Name=user.get('first_name','')+' '+user.get('last_name','')
    if Date_of_Leaving is None:
        Date_of_Leaving='NILL_FOR_NOW'
    if Date_of_Joining is None:
        Date_of_Joining='NILL_FOR_NOW'
    Last_Seen=getLastSeen(user)
    Last_Message=await getLastActivity(User_ID)
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
                
async def makeActivityList():
    async with app:
        async for event in app.get_chat_event_log(TARGET):
            if(event.date.date()>yesterday):
                continue
            if(event.date.date()<yesterday):
                break
            event=json.loads(str(event))
            action=event.get('action').split('.')[1]
            if action=='MEMBER_JOINED' or action=='MEMBER_LEFT':
                activityList.append(event)
        await scrap(activityList)

app.run(makeActivityList())

# PUSHING to JSON
with open('userMaster.json', "w") as file:
    json.dump(userMap, file,indent=4)


# PUSHING to SHEET
result=makeList(userMap)
result.insert(0,['User_ID','FirstName+LastName','User_Name','Date of Joining',	'Date of Leaving','	Last Seen',	'Last Activity'])
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
worksheet = sh.get_worksheet(2)
worksheet.clear()
worksheet.append_rows(result)
worksheet.format('A1:G1', {'textFormat': {'bold': True}})