import os
import logging
import random
import locale

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    AIORateLimiter,
)

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Set locale explicitly to avoid system dependency issues
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    logging.warning("Locale en_US.UTF-8 not available. Using default locale.")

# Load bot token from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# Initialize bot and application
app = Application.builder().token(BOT_TOKEN).rate_limiter(AIORateLimiter()).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to GigaRando!*\n\n"
        "I generate numbers between *1 and 1,000,000,000* at random.\n\n"
        "Press the button below to generate a number!"
    )
    keyboard = [[InlineKeyboardButton("🎲 Generate Number", callback_data="generate_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Callback for button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    if query.data == "generate_number":
        random_number = random.randint(1, 1_000_000_000)
        await query.edit_message_text(f"🎉 Your random number is: *{random_number}*", parse_mode="Markdown")

# Add handlers to the app
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
