import sys
sys.path.append('..')
from pyrogram import Client
import config
import datetime
import json
import re
import gspread
app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
# TARGET='pranav_test_grp'
TARGET='jobcoach_kannada'
todayDate = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=2)
tempUserMap={}
userMap={}
activityList=[]
# with open('firstUserMaster.json') as f:
#    tempUserMap = json.load(f)
# for el in tempUserMap:
#     userMap[el[0]]=el[1:]
    
with open('test.json') as f:
   userMap = json.load(f)

    
def getUserInfoJoin(user,Date_of_Joining):
    User_Name=user.get('username','NOT_AVL')
    Full_Name=user.get('first_name','')+' '+user.get('last_name','')
    Date_of_Leaving='NILL_FOR_NOW'
    Last_Seen=user.get('status','A.NOT_AVILABLE').split('.')[1]
    return [Full_Name,User_Name,Date_of_Joining,Date_of_Leaving,Last_Seen]

def getUserInfoLeave(user,Date_of_Leaving):
    User_Name=user.get('username','NOT_AVL')
    Full_Name=user.get('first_name','')+' '+user.get('last_name','')
    Date_of_Joining='NILL_FOR_NOW'
    Last_Seen=user.get('status','A.NOT_AVILABLE').split('.')[1]
    return [Full_Name,User_Name,Date_of_Joining,Date_of_Leaving,Last_Seen]

def makeList(userMap):
    ans=[]
    for key in userMap:
        temp=userMap[key]
        temp.insert(0,key)
        ans.append(temp)
    return ans

async def makeActivityList():
    async with app:
        async for event in app.get_chat_event_log(TARGET):
            # if(event.date.date()>yesterday):
            #     continue
            if(event.date.date()<yesterday):
                break
            event=json.loads(str(event))
            action=event.get('action').split('.')[1]
            print(action)
            if action=='MEMBER_JOINED' or action=='MEMBER_LEFT':
                activityList.append(event)
app.run(makeActivityList())
                                    
for event in reversed(activityList):
    action=event.get('action').split('.')[1]
    if action=='MEMBER_JOINED':
        print(event['user'].get('first_name') + ' joined')
        id=event['user'].get('id')
        if id in userMap:
            userMap[id][2]=yesterday.strftime("%x")
            userMap[id][3]='NOT_AVL'
        else:
            userMap[id]=getUserInfoJoin(event.get('user'),yesterday.strftime("%x"))
    elif action=='MEMBER_LEFT':
        print(event['user'].get('first_name')+ ' left')
        id=event['user'].get('id')
        if id in userMap:
            userMap[id][3]=yesterday.strftime("%x")
        else:
            print('user not in list')
            userMap[id]=getUserInfoLeave(event.get('user'),yesterday.strftime("%x"))             
# PUSHING to JSON

with open('13_jan.json', "w") as file:
    json.dump(userMap, file)

# result=makeList(userMap)
# gc = gspread.service_account(filename='../secret-key.json')
# sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
# worksheet = sh.get_worksheet(2)
# worksheet.append_rows(result)

