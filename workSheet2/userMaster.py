import sys
sys.path.append('..')
from pyrogram import Client
import config
import datetime
import gspread
import json
app = Client(
    "YOUR_BOT",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
)
TARGET='jobcoach_kannada'
yesterday = datetime.date.today() - datetime.timedelta(days=1)
userList=[]
async def main():
    async with app:
        async for member in app.get_chat_members(TARGET):
            member=json.loads(str(member))
            User_ID=member['user'].get('id')
            User_Name=member['user'].get('username','NOT_AVL')
            Full_Name=member['user'].get('first_name','')+' '+member['user'].get('last_name','')
            Date_of_Joining=member.get('joined_date').split(' ')[0]
            Date_of_Leaving='NILL_FOR_NOW'
            Last_Seen=member['user'].get('status','A.NOT_AVILABLE').split('.')[1]
            if 'last_online_date' in member.get('user'):
                Last_Seen=member['user'].get('last_online_date','A NOT_AVILABLE').split(' ')[1]
            userList.append([User_ID,Full_Name,User_Name,Date_of_Joining,Date_of_Leaving,Last_Seen])

app.run(main())

# PUSHING to JSON
# print(len(userList))
# with open('userMaster.json', "w") as file:
#     json.dump(userList, file)

# PUSHING to SHEET
gc = gspread.service_account(filename='../secret-key.json')
sh = gc.open_by_key('1M00XFS9THpS21bR0TStf6M2rzmnq23CnpXYU69xlW8I')
worksheet = sh.get_worksheet(2)
worksheet.append_rows(userList)

