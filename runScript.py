import schedule
import os
import time
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

def WCB_Data():
    workSheet4 = os.path.join(root_cur_path, 'workSheet6/wcb_data.py')
    os.system('python ' + workSheet4)

schedule.every().day.at(os.getenv('worksheet1_time')).do(contentAnalysis)
schedule.every().day.at(os.getenv('worksheet2_time')).do(user_Master)
schedule.every().day.at(os.getenv('worksheet3_time')).do(user_Data)
schedule.every().day.at(os.getenv('worksheet4_time')).do(telegram_Master)
schedule.every().day.at(os.getenv('worksheet6_time')).do(WCB_Data)

while True:
    schedule.run_pending()
    time.sleep(10)
