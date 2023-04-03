import logging
import json
import os
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, MessageHandler, filters, ContextTypes
                          )
from pydantic import BaseModel, validator
from model import setup, custom_output_parser
import uvicorn
import asyncio

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
class Job(BaseModel):
    title: str

    @validator('title')
    def is_valid_job(cls, value: str):
        valid_jobs = ['data scientist', 'machine learning engineer', 'data analyst', 'data engineer', 'statistician', 'ml researcher', 'data architect', 'data mining engineer', 'applied ml scientist', 'data science manager', 'ml ops engineer', 'data science intern', 'research data scientist', 'senior data scientist', 'lead data scientist', 'principal data scientist', 'chief data scientist', 'business intelligence analyst']
        if value.lower() not in valid_jobs:
            raise ValueError('Oops! Only Data Science and Analytics jobs are allowed for now! You can /start over!')
        return value


logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    """Welcome the user and ask for their job title."""
    await update.message.reply_text("Hi, I am The Data Alchemist, your AI assistant.\nI am here to help you get started with your career growth.\nPlease tell me your job title.")
    return 1

async def job_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the job title and ask for the job level."""
    try:
        job = Job(title=update.message.text)
        context.user_data['job_title'] = job.title
        await update.message.reply_text(f"Got it, your job title is {context.user_data['job_title']}. What is your job level?")
        return 2
    except ValueError as e:
        error_message = e.errors()[0]['msg']
        await update.message.reply_text(error_message)
        return ConversationHandler.END
    
async def job_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the job level and ask for the industry."""
    context.user_data['job_level'] = update.message.text
    await update.message.reply_text(
        "Thanks. Finally, what industry are you looking to work in?")
    return 3

async def industry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the industry and display the gathered information."""
    context.user_data['industry'] = update.message.text
    output = setup(job=context.user_data['job_title'], level=context.user_data['job_level'], industry=context.user_data['industry'])
    list_of_ideas = custom_output_parser(output)
    message = f'Here are 5 projects you can complete to take your career to the next level.\n\n{list_of_ideas[0]}\n\n{list_of_ideas[1]}\n\n{list_of_ideas[2]}\n\n{list_of_ideas[3]}\n\n{list_of_ideas[4]}\n\nGood Luck!'
    await update.message.reply_text(
        f"Here's the information I gathered: \nJob Title: {context.user_data['job_title'].title()}\nJob Level: {context.user_data['job_level'].title()}\nIndustry: {context.user_data['industry'].title()}\n\n{message}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context):
    """Cancel the conversation."""
    await update.message.reply_text('Bye! I canceled the conversation.')
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logging.debug('Update "%s" caused error "%s"', update, context.error)
    await update.message.reply_text(
        "Oops. Something went wrong!🥺"
    )

    
app = FastAPI()
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=job_title)],
        2: [MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=job_level)],
        3: [MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=industry)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    , per_user=True
)


bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
bot.add_handler(conversation_handler)
bot.add_error_handler(error_handler)

@app.post('/', status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(request: Request):
    token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if token != SECRET_TOKEN:
        raise ValueError("Invalid Token. You are not allowed to use this service!")
    payload = await request.body()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty payload")
    json_payload = payload.decode('utf-8')
    try:
        update_dict = json.loads(json_payload)
        update: Update = Update.de_json(update_dict, bot)
        await bot.update_queue.put(update)
    except Exception as e:
        logging.error(f"Failed to parse update: {e}")
    return Response(status_code=status.HTTP_202_ACCEPTED)

@app.get("/home", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Data Alchemist</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f8f9fa;
            }
            .container {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="display-4">The Data Alchemist</h1>
            <p class="lead">Your AI assistant to help you get started with your career growth in Data Science and Analytics.</p>
            <a href="https://t.me/theguy?start=start" class="btn btn-primary">Get Started</a>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


async def telegram_runner():
    bot.run_webhook(
        webhook_url=WEBHOOK_URL,
        secret_token=SECRET_TOKEN,
        port=10000
        )
    
async def fastapi_runner():
    uvicorn.run(app, port=10000)

async def main():
    await asyncio.gather(fastapi_runner(), telegram_runner())
    
if __name__ == '__main__':
    asyncio.run(main())
