import logging
import random
import locale
import os

from flask import Flask, request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    Dispatcher,
)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


locale.setlocale(locale.LC_ALL, '')


BOT_TOKEN = "8148356971:AAHVJWE8RgrP-29a6DgWScnGdzAcptpi_5s"


app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to GigaRando!*\n\n"
        "I generate numbers between *1 and 1,000,000,000* at random.\n\n"
        "🌀 Commands:\n"
        "`/spin` — Quick spin menu\n"
        "`/spin X-Y` — Custom range (e.g., `/spin 10-500`)"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")



async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            min_val, max_val = map(int, context.args[0].split('-'))
            if min_val < 1 or max_val > 1_000_000_000:
                await update.message.reply_text("⚠️ Range must be between 1 and 1,000,000,000")
            elif min_val >= max_val:
                await update.message.reply_text("❌ Max must be greater than Min")
            else:
                await send_random(update, min_val, max_val)
        except:
            await update.message.reply_text("🤔 Usage: `/spin 1-100`", parse_mode="Markdown")
    else:
        keyboard = [
            [
                InlineKeyboardButton("1-100", callback_data="1-100"),
                InlineKeyboardButton("1-1K", callback_data="1-1000")
            ],
            [
                InlineKeyboardButton("1-1M", callback_data="1-1000000"),
                InlineKeyboardButton("1-1B", callback_data="1-1000000000")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎯 Choose a range to spin:", reply_markup=reply_markup)


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        min_val, max_val = map(int, query.data.split('-'))
        await send_random(query.message, min_val, max_val)
    except:
        await query.message.reply_text("⚠️ Invalid range.")



async def send_random(target, min_val: int, max_val: int):
    result = random.randint(min_val, max_val)
    formatted_result = locale.format_string("%d", result, grouping=True)
    formatted_min = locale.format_string("%d", min_val, grouping=True)
    formatted_max = locale.format_string("%d", max_val, grouping=True)

    msg = (
        "🎰 *GigaRando Spin Result* 🎰\n\n"
        f"From: `{formatted_min}`\n"
        f"To: `{formatted_max}`\n\n"
        f"✨ *{formatted_result}* ✨"
    )
    await target.reply_text(msg, parse_mode="Markdown")


# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("spin", spin))
application.add_handler(CallbackQueryHandler(handle_button))



@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"



@app.route('/')
def home():
    return "✅ GigaRandoBot is running!"



if __name__ == '__main__':
    import asyncio

    async def run():
        await application.initialize()
        await application.start()
        port = int(os.environ.get("PORT", 10000))
        app.run(host='0.0.0.0', port=port)

    asyncio.run(run())
