import sys,os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import gspread
import json
sys.path.append(os.getcwd())
from db.db_model import DynamoDB_con
DB = DynamoDB_con()
quiz_number=0

with open('workSheet7/quiz_number.json') as f:
   quiz_number = json.load(f)[0]+1

def refactor(obj):
    quizNumber=int(obj['quiz_no'])
    Date=obj['timestamp'].split('.')[0].split('T')[0]
    correctAnswers=obj['correct_answers']
    quizEngagement=obj['engagement']
    res=[Date,quizNumber]
    for el in quizEngagement:
        res.append(int(el))
    for el in correctAnswers:
        res.append(int(el))
    return res

# READING FROM DynamoDB
sheetData=DB.read_data('TB_QuizBot_Engagement','quiz_no',quiz_number)
sheetData=list(map(refactor,sheetData))

with open('workSheet7/quiz_number.json', "w") as file:
    json.dump([quiz_number], file,indent=4)

# PUSHING to SHEET
gc = gspread.service_account(filename=os.path.join(os.getcwd() +'/secret-key.json'))
sh = gc.open_by_key(os.getenv('SHEET_ID'))
worksheet = sh.worksheet('Quiz_Data')
worksheet.append_rows(sheetData)
print('scrapping in workSheet7 done, successfully')