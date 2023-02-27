import sys,os
from dotenv import load_dotenv
load_dotenv()
import datetime
import json
import gspread
sys.path.append(os.getcwd())
from config import * 

cur_path = os.path.dirname(__file__)
group_chat_id=os.getenv('GROUP_CHAT_ID')
joinByInvite='UNKNOWN-types.ChannelAdminLogEventActionParticipantJoinByInvite'
currentTime=datetime.datetime.now()
today=datetime.date.today()
isMorningShift=True
yesterday = today - datetime.timedelta(days=1)
userMap={}
activityList=[]
messageList=[]
if(currentTime.hour>=12):
    print('Scrapping for Evening Shift')
    isMorningShift=False
else:
    print('Scrapping for Morning Shift')
    
def refactored_obj(obj):
    fullName=obj['Full_Name']
    userName=obj['User_Name']
    dateOfJoining=obj['Date_of_Joining']
    dateOfLeaving=obj['Date_of_Leaving']
    lastSeen=obj['Last_Seen']
    lastActivity=obj['Last_Activity']
    return [fullName,userName,dateOfJoining,dateOfLeaving,lastSeen,lastActivity]

sheetData=DB.read_all_data(user_master)
for el in sheetData:
    userMap[str(el['User_ID'])]=refactored_obj(el)

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
        temp.insert(0,int(key))
        ans.append(temp)
    return ans
 
async def scrap(activityList):        
    for event in reversed(activityList):
        action=event.get('action').partition(".")[2]
        if action=='MEMBER_JOINED' or action==joinByInvite:
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
        async for event in app.get_chat_event_log(group_chat_id):
            if isMorningShift:
                if(event.date.date()>yesterday):
                    continue
                if(event.date.date()<yesterday):
                    break
            else:
                if(event.date.date()<today):
                    break
            event=json.loads(str(event))
            action=event.get('action').partition(".")[2]
            if action=='MEMBER_JOINED' or action=='MEMBER_LEFT' or action=='USERNAME_CHANGED' or action==joinByInvite:
                activityList.append(event)
            
        await scrap(activityList)
            
        async for message in app.get_chat_history(group_chat_id):
            if isMorningShift:
                if(message.date.date()>yesterday):
                    continue
                if(message.date.date()<yesterday):
                    break
            else:
                if(message.date.date()<today):
                    break
            message=json.loads(str(message))
            messageList.append(message)
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

result=makeList(userMap)
result=sorted(result, key = lambda x: x[3])

if isMorningShift:
    DB.deleteTotalData(user_master)
    for el in result:
        dataFormat={
            'User_ID':str(el[0]),
            'Full_Name':el[1],
            'User_Name':el[2],
            'Date_of_Joining':el[3],
            'Date_of_Leaving':el[4],
            'Last_Seen':el[5],
            'Last_Activity':el[6],
        }
        DB.send_data(dataFormat,user_master)
print(f"Data from {user_master}")

# PUSHING to SHEET
result.insert(0,['User_ID','FirstName+LastName','User_Name','Date of Joining',	'Date of Leaving','	Last Seen',	'Last Activity'])
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('User_Master')
worksheet.clear()
worksheet.append_rows(result)
print('scrapping in workSheet2 done, successfully')
