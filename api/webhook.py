import os
import logging
import random
import locale
import json

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    AIORateLimiter,
)

# Setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
locale.setlocale(locale.LC_ALL, '')

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(BOT_TOKEN)
app = Application.builder().token(BOT_TOKEN).rate_limiter(AIORateLimiter()).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to GigaRando!*\n\n"
        "I generate numbers between *1 and 1,000,000,000* at random.\n\n"
