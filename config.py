import sys,os
from dotenv import load_dotenv
load_dotenv()
from pyrogram import Client
from db.db_model import DynamoDB_con
DB = DynamoDB_con()
app = Client("YOUR_BOT")
content_analysis=os.getenv('content_analysis')
user_master=os.getenv('user_master')
user_data=os.getenv('user_data')
telegram_master=os.getenv('telegram_master')
wcb_data=os.getenv('wcb_data')
jumbledword_bank=os.getenv('jumbledword_bank')
jumbledword_engagement=os.getenv('jumbledword_engagement')
quizbot_bank=os.getenv('quizbot_bank')
quizbot_engagement=os.getenv('quizbot_engagement')
quizbot_polls=os.getenv('quizbot_polls')
quizbot_session=os.getenv('quizbot_session')
storybuilding_bank=os.getenv('storybuilding_bank')
storybuilding_data=os.getenv('storybuilding_data')
temp_jumbledword_session=os.getenv('temp_jumbledword_session')
user_points=os.getenv('user_points')