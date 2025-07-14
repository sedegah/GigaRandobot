import os
import logging
import random
import locale

from fastapi import FastAPI, Request, HTTPException
import uvicorn

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    constants,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    AIORateLimiter,
    ContextTypes,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Set locale explicitly (this can prevent issues on some systems)
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    logger.warning("Locale en_US.UTF-8 not available. Using default locale.")

# Load environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN environment variable not set!")
if not WEBHOOK_URL:
    logger.error("WEBHOOK_URL environment variable not set!")
    raise ValueError("WEBHOOK_URL environment variable not set!")

# Initialize FastAPI app
app = FastAPI(title="GigaRandoBot Webhook")

# Build the Telegram bot application (using async and rate limiter)
tg_app = Application.builder().token(BOT_TOKEN).rate_limiter(AIORateLimiter()).build()


# /start command handler: Sends a welcome message and a button to generate a number
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to GigaRando!*\n\n"
        "I generate numbers between *1 and 1,000,000,000* at random.\n\n"
        "Press the button below to generate a number!"
    )
    keyboard = [
        [InlineKeyboardButton("🎲 Generate Number", callback_data="generate_number")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(
            text=welcome_text, reply_markup=reply_markup, parse_mode=constants.ParseMode.MARKDOWN
        )
    else:
        logger.warning("Received /start command without a message.")


# Callback for button presses: Generates a random number and sends it
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge callback query
    if query.data == "generate_number":
        random_number = random.randint(1, 1_000_000_000)
        await query.edit_message_text(
            text=f"🎉 Your random number is: *{random_number}*",
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    else:
        logger.warning(f"Unknown callback data: {query.data}")


# Register handlers with the Telegram application
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CallbackQueryHandler(button_handler))


# FastAPI route to receive Telegram webhook updates
@app.post("/webhook")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
    except Exception as e:
        logger.error("Failed to parse request body: %s", e)
        raise HTTPException(status_code=400, detail="Invalid JSON")

    logger.info("Received update: %s", data)
    try:
        update = Update.de_json(data, tg_app.bot)
    except Exception as e:
        logger.error("Error parsing update: %s", e)
        raise HTTPException(status_code=400, detail="Error parsing update")

    # Process the update asynchronously via the bot
    try:
        await tg_app.process_update(update)
    except Exception as e:
        logger.exception("Exception while processing update: %s", e)
        # Optionally, return an error or simply log the exception.
    return {"status": "ok"}


# On startup, register the webhook with Telegram
@app.on_event("startup")
async def on_startup():
    try:
        # Set webhook for Telegram bot
        await tg_app.bot.set_webhook(WEBHOOK_URL)
        logger.info("Webhook successfully set to: %s", WEBHOOK_URL)
    except Exception as e:
        logger.exception("Failed to set webhook: %s", e)
        # Depending on your deployment strategy, you might want to exit here
        raise e


# Entry point: Run with uvicorn if executed directly
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    logger.info("Starting uvicorn server on port %s", PORT)
    uvicorn.run("api.webhook:app", host="0.0.0.0", port=PORT, log_level="info")
