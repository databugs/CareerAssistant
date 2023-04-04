
# AI Career Assistant

AI-powered career growth assistant for Data Science and Analytics.




## How To Use the Bot
Using the bot is straight forward. You must have telegram installed.

Get started [here](https://dataalchemist.onrender.com/)

After opening the bot, click on `start` or type and send `/start` to get started.

The bot will ask for your job title, level, and Industry. It will then use the information it has gathered to generate a list of projects you can do to take your career to the next level.

## Technology
- langchain
- Open AI
- python-telegram-bot
- FastApi
- Render (Webhook)
## Installation

1. Create a folder
```
    mkdir mynewfolder
```
2. Change directory to the new folder
```
    cd mynewfolder
```
3. Clone this repository
```
    git clone https://github.com/databugs/CareerAssistant.git

```
3. Change directory to CareerAssistant
```
    cd CareerAssistant
```
4. Create and activate a virtual environment
```
    python -m venv env && .\env\Scripts\activate
```
5. Run this to install all requirements
```
    pip install -r requirements.txt
```
6. Start the server
```
    python main.py
```
## Environmental Variables
Here is a list of all the environmental variables used here:
- **telegram token**: you need this to communicate with the telegram's api.
- **openai api-key**: you need this to to interact with all the text models they provide.
- **secret-token**: this token helps us to validate that the update we are recieving is in fact coming from our bot.
- **webhook url**: all updates from telegram are sent to this url.

## Note
The bot is live [here](https://dataalchemist.onrender.com/). It is presently using my OpenAI api-key. Alternative options are under development.

## Roadmap
- [] Add the option to use this without webhook
- [] Add a conversational and memory feature
