# telegram_notifier.py

import os
import requests
from dotenv import load_dotenv
from notifier import Notifier

class TelegramNotifier(Notifier):
    def __init__(self):
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")

    def escape_markdown(self, text):
        for char in r"_*[]()~`>#+-=|{}.!" :
            text = text.replace(char, f"\\{char}")
        return text

    def send(self, message: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "MarkdownV2"
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()

