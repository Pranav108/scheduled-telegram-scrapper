import schedule
import os
cur_path = os.path.dirname(__file__)

def contentAnalysis():
    workSheet1 = os.path.join(cur_path, 'workSheet1/scrap.py')
    os.system('python ' + workSheet1)
    
def user_Master():
    workSheet2 = os.path.join(cur_path, 'workSheet2/eventUpdate.py')
    os.system('python ' + workSheet2)
    
def user_Data ():
    workSheet3 = os.path.join(cur_path, 'workSheet3/userData.py')
    os.system('python ' + workSheet3)
    
def telegram_Master():
    workSheet4 = os.path.join(cur_path, 'workSheet4/telegramMaster.py')
    os.system('python ' + workSheet4)

schedule.every().day.at("04:00").do(contentAnalysis)
schedule.every().day.at("04:10").do(user_Master)
schedule.every().day.at("04:20").do(user_Data)
schedule.every().day.at("04:30").do(telegram_Master)
schedule.run_all()
schedule.run_all(delay_seconds=600)