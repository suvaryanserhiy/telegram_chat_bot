from flask import Flask
from threading import Thread
import os
from bot import app

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 Telegram bot is running!"

if __name__ == "__main__":
    # Flask goes in the background thread: the bot's polling loop needs the main thread for its signal handlers
    port = int(os.environ.get("PORT", 10000))
    Thread(target=flask_app.run, kwargs={"host": "0.0.0.0", "port": port}, daemon=True).start()

    app.run_polling()
