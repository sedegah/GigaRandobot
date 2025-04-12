# api/webhook.py
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.ext import AIORateLimiter
from telegram.ext.webhook import WebhookServer
import logging
import json

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(BOT_TOKEN)
app = Application.builder().token(BOT_TOKEN).rate_limiter(AIORateLimiter()).build()

# Define your command handlers here (like start, spin, etc.)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GigaRandoBot is alive!")

app.add_handler(CommandHandler("start", start))

# Main handler for Vercel
async def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method not allowed"}

    body = await request.body()
    update = Update.de_json(json.loads(body), bot)
    await app.process_update(update)
    return {"statusCode": 200, "body": "OK"}
