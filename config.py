import configparser

config_data = configparser.ConfigParser()
config_data.read("config.ini")
tables = config_data["tables"]

content_analysis=tables.get('content_analysis')
user_master=tables.get('user_master')
user_data=tables.get('user_data')
telegram_master=tables.get('telegram_master')
wcb_data=tables.get('wcb_data')
jumbledword_bank=tables.get('jumbledword_bank')
jumbledword_engagement=tables.get('jumbledword_engagement')
quizbot_bank=tables.get('quizbot_bank')
quizbot_engagement=tables.get('quizbot_engagement')
quizbot_polls=tables.get('quizbot_polls')
quizbot_session=tables.get('quizbot_session')
storybuilding_bank=tables.get('storybuilding_bank')
storybuilding_data=tables.get('storybuilding_data')
temp_jumbledword_session=tables.get('temp_jumbledword_session')
user_points=tables.get('user_points')