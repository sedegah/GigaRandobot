from flask import Flask, request
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Initialize the Flask app
app = Flask(__name__)

# Your Telegram Bot Token and Webhook URL
TELEGRAM_BOT_TOKEN = "8148356971:AAGX-iBFu-yxUjq_yzNnn2QGrBT1Lcz6yy4"
WEBHOOK_URL = "https://gigarandobot.railway.app/webhook"  # Ensure this uses HTTPS

# Initialize the Bot and Dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Define your command handler or message handler
def start(update, context):
    update.message.reply_text('Hello, I am your bot!')

# Add handler to dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# Webhook route for Telegram to send updates
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    dispatcher.process_update(update)
    return "OK", 200

# Set the webhook for Telegram to send updates to
bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, port=5000)
