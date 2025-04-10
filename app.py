from flask import Flask, request
import json
from telegram import Bot
from telegram.ext import Updater

# Initialize the Flask app
app = Flask(__name__)

# Telegram bot token and webhook URL
TELEGRAM_BOT_TOKEN = "8148356971:AAGX-iBFu-yxUjq_yzNnn2QGrBT1Lcz6yy4"  # Replace with your Telegram bot token
WEBHOOK_URL = "https://gigarandobot.railway.app/webhook"  # Replace with your Railway app's HTTPS URL

# Initialize the Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Set the webhook URL for the bot
bot.set_webhook(url=WEBHOOK_URL)

# Define the webhook route to handle incoming updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    data = request.get_json()
    print("Received data:", data)
    # You can process the incoming update here
    return "OK", 200

if __name__ == "__main__":
    # Run the app on the designated port (e.g., 5000 for Railway)
    app.run(debug=True, port=5000)
