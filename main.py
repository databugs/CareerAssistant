import logging
import json
import os

from fastapi import FastAPI, Request, Response, HTTPException, status

from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          ConversationHandler, MessageHandler, filters, ContextTypes
                          )


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

app = FastAPI()
    
bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

logging.basicConfig(level=logging.INFO)

@app.post('/', status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(request: Request):
    payload = await request.body()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty payload")
    json_payload = payload.decode('utf-8')
    try:
        update_dict = json.loads(json_payload)
        update = Update.de_json(update_dict, bot)
        logging.info(f"Received Telegram update: {update}")
        logging.info(f"Type of Telegram Update: {type(update)}")
    except Exception as e:
        logging.error(f"Failed to parse update: {e}")
    return Response(status_code=status.HTTP_202_ACCEPTED)
