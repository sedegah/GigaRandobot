import requests

BOT_TOKEN = "8148356971:AAHVJWE8RgrP-29a6DgWScnGdzAcptpi_5s"
WEBHOOK_URL = "https://gigarandobot.onrender.com/webhook"

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
)

print("Webhook response:")
print(response.json())
