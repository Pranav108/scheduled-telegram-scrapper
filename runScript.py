import schedule
import os
import time
import datetime
import db.create_db
from config import * 
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

root_cur_path = Path(os.path.dirname(__file__)).absolute()

def contentAnalysis():
    workSheet1 = os.path.join(root_cur_path, 'workSheet1/scrap.py')
    os.system('python ' + workSheet1)
    
def user_Master():
    workSheet2 = os.path.join(root_cur_path, 'workSheet2/eventUpdate.py')
    os.system('python ' + workSheet2)
    
def user_Data ():
    workSheet3 = os.path.join(root_cur_path, 'workSheet3/userData.py')
    os.system('python ' + workSheet3)
    
def telegram_Master():
    workSheet4 = os.path.join(root_cur_path, 'workSheet4/telegramMaster.py')
    os.system('python ' + workSheet4)

def JWB_Data():
    workSheet5 = os.path.join(root_cur_path, 'workSheet5/jwb_data.py')
    os.system('python ' + workSheet5)

def WCB_Data():
    workSheet6 = os.path.join(root_cur_path, 'workSheet6/wcb_data.py')
    os.system('python ' + workSheet6)

def quizBotEngagement():
    workSheet7 = os.path.join(root_cur_path, 'workSheet7/quiz_botEng.py')
    os.system('python ' + workSheet7)
    
def storyBuilding():
    workSheet8 = os.path.join(root_cur_path, 'workSheet8/story_building.py')
    os.system('python ' + workSheet8)

currentTime=datetime.datetime.now()
today=datetime.date.today()


def parentCaller():
    time.sleep(20)
    user_Master()
    if(currentTime.hour<12):
        contentAnalysis()
        time.sleep(20)
        user_Data()
        time.sleep(20)
        telegram_Master()
        time.sleep(20)
        JWB_Data()
        time.sleep(20)
        WCB_Data()
        time.sleep(20)
        quizBotEngagement()
        time.sleep(20)
        storyBuilding()
    print('All sheet updated')
    
schedule.every().day.at(os.getenv('running_time')).do(parentCaller)
schedule.run_all(delay_seconds=86400)
