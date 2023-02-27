import sys,os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import datetime
import gspread
import json
sys.path.append(os.getcwd())
from config import * 

yesterday = datetime.date.today() - datetime.timedelta(days=1)
def refactor(obj):
    quizNumber=int(obj['quiz_no'])
    Date=obj['date']
    correctAnswers=obj['correct_answers']
    quizEngagement=obj['engagement']
    res=[Date,quizNumber]
    for el in quizEngagement:
        res.append(int(el))
    for el in correctAnswers:
        res.append(int(el))
    return res

# READING FROM DynamoDB
yesterday_str=yesterday.strftime('%Y-%m-%d')
sheetData=DB.read_data(quizbot_engagement,'date',yesterday_str)
sheetData=list(map(refactor,sheetData))

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('Quiz_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet7 done, successfully')