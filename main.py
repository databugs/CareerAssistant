import logging
import json
import os

from fastapi import FastAPI, Request, Response, HTTPException, status

from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, MessageHandler, filters, ContextTypes
                          )
from pydantic import BaseModel, validator

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

class Job(BaseModel):
    title: str

    @validator('title')
    def is_valid_job(cls, value: str):
        valid_jobs = ['data scientist', 'machine learning engineer', 'data analyst', 'data engineer', 'statistician', 'ml researcher', 'data architect', 'data mining engineer', 'applied ml scientist', 'data science manager', 'ml ops engineer', 'data science intern', 'research data scientist', 'senior data scientist', 'lead data scientist', 'principal data scientist', 'chief data scientist', 'business intelligence analyst']
        if value.lower() not in valid_jobs:
            raise ValueError('Oops! Only Data Science and Analytics jobs are allowed for now! You can /start over!')
        return value


app = FastAPI()
logging.basicConfig(level=logging.INFO)
    
bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

@app.post('/', status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(request: Request):
    payload = await request.body()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty payload")
    json_payload = payload.decode('utf-8')
    try:
        update_dict = json.loads(json_payload)
        update: Update = Update.de_json(update_dict, bot)
        logging.info(f"Received Telegram update: {update}")
        logging.info(f"Type of Telegram Update: {type(update)}")
        await bot.process_update(update)
    except Exception as e:
        logging.error(f"Failed to parse update: {e}")
    return Response(status_code=status.HTTP_202_ACCEPTED)

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
    #output = setup(job=context.user_data['job_title'], level=context.user_data['job_level'], industry=context.user_data['industry'])
    #list_of_ideas = custom_output_parser(output)
    #message = f'Here are 5 projects you can complete to take your career to the next level.\n\n{list_of_ideas[0]}\n\n{list_of_ideas[1]}\n\n{list_of_ideas[2]}\n\n{list_of_ideas[3]}\n\n{list_of_ideas[4]}\n\nGood Luck!'
    await update.message.reply_text(
        f"Here's the information I gathered: \nJob Title: {context.user_data['job_title'].title()}\nJob Level: {context.user_data['job_level'].title()}\nIndustry: {context.user_data['industry'].title()}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context):
    """Cancel the conversation."""
    await update.message.reply_text('Bye! I canceled the conversation.')
    return ConversationHandler.END

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logging.debug('Update "%s" caused error "%s"', update, context.error)


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

bot.add_handler(conversation_handler)
bot.add_handler(error)