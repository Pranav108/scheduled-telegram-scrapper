import sys,os
from dotenv import load_dotenv
load_dotenv()
from pyrogram import Client
import datetime
import gspread
import json
sys.path.append(os.getcwd())
from db.db_model import DynamoDB_con
DB = DynamoDB_con()

cur_path = os.path.dirname(__file__)
app = Client(
    "YOUR_BOT",
    api_id = os.getenv('API_ID'),
    api_hash = os.getenv('API_HASH')
)
TARGET='jobcoach_kannada'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
messageList=[]
userMap={}

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
            print(Last_Message)
    return Last_Message

def makeList(userMap):
    ans=[]
    for key in userMap:
        temp=userMap[key]
        temp.insert(0,key)
        ans.append(temp)
    return ans

async def main():
    async with app:
        async for member in app.get_chat_members(TARGET):
            member=json.loads(str(member))
            User_ID=member['user'].get('id')
            User_Name=member['user'].get('username','NOT_AVL')
            Full_Name=member['user'].get('first_name','')+' '+member['user'].get('last_name','')
            Date_of_Joining=member.get('joined_date')
            
            if Date_of_Joining is None:
                Date_of_Joining='OWNER'
            else:
                Date_of_Joining=Date_of_Joining.split(' ')[0]
            Date_of_Leaving='NILL_FOR_NOW'
            Last_Seen=getLastSeen(member['user'])
            Last_Message=await getLastActivity(User_ID)
            userMap[User_ID]=[Full_Name,User_Name,Date_of_Joining,Date_of_Leaving,Last_Seen,Last_Message]

app.run(main())
# print(len(messageList))
# PUSHING to JSON
print(len(userMap))
# with open(os.path.join(cur_path, 'userMaster.json'), "w") as file:
#     json.dump(userMap, file)

# result=makeList(userMap)
# PUSHING to SHEET
# Run this to ONLY to clear the left members data
# gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
# sh = gc.open_by_key(os.getenv('SHEET_ID'))
# worksheet = sh.get_worksheet(2)
# worksheet.append_rows(result)

