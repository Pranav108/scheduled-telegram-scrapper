# Telegram Scarpping

A Python script to scrap Various data from the telegram group.

## Features

- Extract data based on ,user, date, activity,
- Scrap data on Daily Basic.
- Push the data to google spreadSheet in readable format.
- Push the Data to DynamoDB as well.

## Tech stacks

- Python - programming language
- DynamoDB - hosted NoSQL database offered by AWS
- Google Cloud - suite of cloud computing services.
- Git - version control system

## Setting Up Your Local Environment

If you wish to play around with the code base in your local environment, do the following

```bash
* Clone this repo to your local machine.
* Using the terminal, navigate to the cloned repo.
* Install all the neccessary dependencies, as stipulated in the requirements.txt file.
* Get your API_HASH and API_ID from my.telegram.org.
* Connect you googleSheet with bot to edit your sheet and get it's credentials.
```

In your .env file, set environment variables for the following:

```properties
# TELEGRAM CREDENTIALS
API_ID =
API_HASH =
GROUP_CHAT_ID =

# GOOGLE SHEET ID
SHEET_ID =

# DYNAMO_DB THINGS
service_name =
region_name =
aws_access_key_id =
aws_secret_access_key =
API_KEY =
bot_username =
```

Helpful commands

```bash
$ git clone https://github.com/yourGitHubUsername/scheduled-telegram-scrapper.git
$ cd scheduled-telegram-scrapper
$ pip3 install -r requirements.txt
$ python runScript.py
```

## Author

- [@Pranav108](https://github.com/Pranav108/) 🙋‍♂️
