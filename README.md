## GigaRandoBot

**GigaRandoBot** is a Telegram bot that generates random numbers between 1 and 1,000,000,000 on demand. Built using **FastAPI** and **python-telegram-bot**, it offers a smooth, interactive experience via webhook updates.

---

### Overview

The bot responds to the `/start` command with an inline button that, when clicked, triggers the generation and delivery of a random number. Webhook delivery is handled through an async FastAPI server with rate-limiting support enabled.

---

### Tech Stack

* **Python 3.11**
* **FastAPI** — webhook server
* **python-telegram-bot 20.7** — Telegram bot framework (async)
* **AIORateLimiter** — optional per-user request throttling
* **Uvicorn** — ASGI server for FastAPI

---

### Functional Handlers

* `/start`: Sends a welcome message with a button
* `callback_query:generate_number`: Replies with a random integer

---

### Code Structure

```
.
├── api/
│   └── webhook.py        
├── requirements.txt     
├── runtime.txt          
├── README.md            
```

---

### Environment Configuration

This project relies on the following environment variables:

* `BOT_TOKEN`: Telegram Bot API token
* `WEBHOOK_URL`: Full HTTPS webhook URL for Telegram to send updates
* `PORT`: Optional (default is 10000)

These variables are used for both webhook registration and runtime execution.

---

### Deployment Notes

* The webhook is automatically registered on startup using the provided `WEBHOOK_URL`.
* The app runs on `uvicorn` and listens on the port defined by the environment.
* Inline command and callback interactions are processed via `telegram.ext.Application`.

---

### Command Overview

| Command    | Triggered Action                               |
| ---------- | ---------------------------------------------- |
| `/start`   | Sends welcome text with a generate button      |
| `callback` | Returns a random number when button is clicked |

---

### License

This project is licensed under the MIT License.

