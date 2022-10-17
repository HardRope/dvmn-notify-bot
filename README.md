# -dvmn-notify-bot

This program created to send you notifications about new reviewed works from [Devman](https://dvmn.org/)
## How to use

To use script, you need to create `.env` with some tokens:
* DVMN_TOKEN=[Devman](https://dvmn.org/api/docs/) API token
* TG_TOKEN=telegram bot token
* CHAT_ID=your telegram chat id

Help with obtain TG-Token: [Bot Father](https://telegram.me/BotFather)

Help with obtain your chat_id: [userinfobot](https://t.me/userinfobot)


Python3 should be already installed. Then use pip (or `pip3`, if there is a conflict with Python2) to install dependencies:

```commandline
pip install -r requirements.txt
```

To run the cheking notifies, just run script from your console:

```commandline
python notify_sender.py
```

## Result

When your work has been reviewed, bot send you message:

![img.png](message_example.png)

## Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org.
