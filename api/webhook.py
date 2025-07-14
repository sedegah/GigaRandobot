import os
import logging
import random
import locale

from fastapi import FastAPI, Request, HTTPException
import uvicorn

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, constants
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, AIORateLimiter, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    logger.warning("Locale en_US.UTF-8 not available. Using default locale.")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN environment variable not set!")

if not WEBHOOK_URL:
    logger.error("WEBHOOK_URL environment variable not set!")
    raise ValueError("WEBHOOK_URL environment variable not set!")

app = FastAPI(title="GigaRandoBot Webhook")
tg_app = Application.builder().token(BOT_TOKEN).rate_limiter(AIORateLimiter()).build()

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
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode=constants.ParseMode.MARKDOWN
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "generate_number":
        random_number = random.randint(1, 1_000_000_000)
        await query.edit_message_text(
            text=f"🎉 Your random number is: *{random_number}*",
            parse_mode=constants.ParseMode.MARKDOWN,
        )

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CallbackQueryHandler(button_handler))

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

    if not tg_app._initialized:
        await tg_app.initialize()

    try:
        await tg_app.process_update(update)
    except Exception as e:
        logger.exception("Exception while processing update: %s", e)

    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "GigaRandoBot is alive!"}


@app.on_event("startup")
async def on_startup():
    try:
        await tg_app.initialize()
        await tg_app.bot.set_webhook(WEBHOOK_URL)
        logger.info("Webhook successfully set to: %s", WEBHOOK_URL)
    except Exception as e:
        logger.exception("Failed to set webhook: %s", e)
        raise e

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    logger.info("Starting uvicorn server on port %s", PORT)
    uvicorn.run("api.webhook:app", host="0.0.0.0", port=PORT, log_level="info")
